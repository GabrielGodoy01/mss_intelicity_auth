from aws_cdk import (
    aws_lambda as lambda_,
    Duration
)
from constructs import Construct
from aws_cdk.aws_apigateway import Resource, LambdaIntegration, CognitoUserPoolsAuthorizer


class LambdaStack(Construct):
    functions_that_need_cognito_permissions = []

    def create_lambda_api_gateway_integration(self, module_name: str, method: str, api_resource: Resource,
                                              environment_variables: dict = {"STAGE": "TEST"}, authorizer=None):

        function = lambda_.Function(
            self, module_name.title(),
            code=lambda_.Code.from_asset(f"../src/modules/{module_name}"),
            handler=f"app.{module_name}_presenter.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            layers=[self.lambda_layer],
            memory_size=512,
            environment=environment_variables,
            timeout=Duration.seconds(15)
        )

        api_resource.add_resource(module_name.replace("_", "-")).add_method(method,
                                                                                       integration=LambdaIntegration(
                                                                                           function))

        return function

    def __init__(self, scope: Construct, api_gateway_resource: Resource, environment_variables: dict,
                 authorizer: CognitoUserPoolsAuthorizer = None) -> None:
        super().__init__(scope, "Auth_Lambda")

        self.lambda_layer = lambda_.LayerVersion(self, "Auth_Layer",
                                                 code=lambda_.Code.from_asset("./lambda_layer_out_temp"),
                                                 compatible_runtimes=[lambda_.Runtime.PYTHON_3_9]
                                                 )
        

        self.check_token = self.create_lambda_api_gateway_integration(
            module_name="check_token",
            method="POST",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            # authorizer=authorizer
        )

        self.create_user = self.create_lambda_api_gateway_integration(
            module_name="create_user",
            method="POST",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            # authorizer=authorizer
        )

        self.list_users_in_group = self.create_lambda_api_gateway_integration(
            module_name="list_users_in_group",
            method="POST",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            # authorizer=authorizer
        )

        self.update_user = self.create_lambda_api_gateway_integration(
            module_name="update_user",
            method="POST",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            # authorizer=authorizer
        )

        self.functions_that_need_cognito_permissions = [
            self.check_token,
            self.create_user,
            self.list_users_in_group,
            self.update_user
        ]