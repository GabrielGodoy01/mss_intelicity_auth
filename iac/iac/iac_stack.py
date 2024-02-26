import os
from aws_cdk import (
    aws_lambda as lambda_,
    Stack,
    aws_cognito,
    Duration,
    aws_iam
)
from constructs import Construct
from .lambda_stack import LambdaStack
from aws_cdk.aws_apigateway import RestApi, Cors, CognitoUserPoolsAuthorizer


class IacStack(Stack):
    lambda_stack: LambdaStack

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.user_pool_arn = os.environ.get("USER_POOL_ARN")
        self.github_ref_name = os.environ.get("GITHUB_REF_NAME")
        self.aws_region = os.environ.get("AWS_REGION")
        self.user_pool_name = os.environ.get("USER_POOL_NAME")
        self.user_pool_id = os.environ.get("USER_POOL_ID")

        if 'prod' in self.github_ref_name:
            stage = 'PROD'

        elif 'homolog' in self.github_ref_name:
            stage = 'HOMOLOG'

        else:
            stage = 'DEV'

        # self.cognito_auth = CognitoUserPoolsAuthorizer(self, f"auth_{self.github_ref_name}",
        #                                                cognito_user_pools=[aws_cognito.UserPool.from_user_pool_arn(
        #                                                    self, f"authentication-{self.github_ref_name}", self.user_pool_arn
        #                                                )]
        #                                                )


        self.rest_api = RestApi(self, f"AuthProfile_RestApi_{self.github_ref_name}",
                                rest_api_name=f"AuthProfile_RestApi_{self.github_ref_name}",
                                description="This is the AuthProfile RestApi",
                                default_cors_preflight_options={
                                    "allow_origins": Cors.ALL_ORIGINS,
                                    "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                                    "allow_headers": ["*"]
                                },
                                )

        api_gateway_resource = self.rest_api.root.add_resource("mss-auth", default_cors_preflight_options={
            "allow_origins": Cors.ALL_ORIGINS,
            "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": Cors.DEFAULT_HEADERS
        }
        )

        ENVIRONMENT_VARIABLES = {
            "STAGE": stage,
            "USER_POOL_ID":  self.user_pool_id,
            "USER_POOL_NAME": self.user_pool_name
        }

        self.lambda_stack = LambdaStack(self, api_gateway_resource=api_gateway_resource,
                                        environment_variables=ENVIRONMENT_VARIABLES)
        
        cognito_admin_policy = aws_iam.PolicyStatement(
            effect=aws_iam.Effect.ALLOW,
            actions=[
                "cognito-idp:*",
            ],
            resources=[
                self.user_pool_arn
            ]
        )

        for f in self.lambda_stack.functions_that_need_cognito_permissions:
            f.add_to_role_policy(cognito_admin_policy)