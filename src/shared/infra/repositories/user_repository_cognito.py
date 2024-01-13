import json
from typing import Tuple, List

import boto3
from botocore.exceptions import ClientError

from src.shared.domain.entities.user import User
from src.shared.domain.enums.groups_enum import GROUPS
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, ForbiddenAction, InvalidTokenError
from src.shared.infra.dtos.user_cognito_dto import UserCognitoDTO


class UserRepositoryCognito(IUserRepository):

    client: boto3.client
    user_pool_id: str
    client_id: str

    def __init__(self):
        self.client = boto3.client('cognito-idp', region_name="sa-east-1")
        self.user_pool_id = "sa-east-1_BM8l9PeRZ";
        self.client_id = "1791soos64mqql1bors992jk43"

    
    def get_user_by_email(self, email: str) -> User:
        try:
            response = self.client.admin_get_user(
                UserPoolId=self.user_pool_id,
                Username=email
            )
            if response["UserStatus"] == "UNCONFIRMED":
                return None

            user = UserCognitoDTO.from_cognito(response).to_entity()
            groupResponse = self.client.admin_list_groups_for_user(
                Username=user.email,
                UserPoolId=self.user_pool_id,
            )

            for group in groupResponse.get('Groups'):
                user.groups.append(GROUPS(group.get('GroupName')))
                
            return user

        except self.client.exceptions.UserNotFoundException:
            return None
    
    def create_user(self, user: User) -> User:
        cognito_attributes = UserCognitoDTO.from_entity(user).to_cognito_attributes()
        try:

            self.client.admin_create_user(
                UserPoolId=self.user_pool_id,
                Username=user.email,
                DesiredDeliveryMediums="EMAIL",
                UserAttributes=cognito_attributes)
            
            for group in user.groups:
                self.client.admin_add_user_to_group(
                    UserPoolId=self.user_pool_id,
                    Username=user.email,
                    GroupName=group.value
                )

        except self.client.exceptions.UsernameExistsException:
            raise DuplicatedItem("user")

        except self.client.exceptions.InvalidParameterException as e:
            raise EntityError(e.response.get('Error').get('Message'))

        return user
    
    def check_token(self, token: str) -> User:
        try:
            userResponse = self.client.get_user(
                AccessToken=token
            )

            user = UserCognitoDTO.from_cognito(userResponse).to_entity()

            groupResponse = self.client.admin_list_groups_for_user(
                Username=user.email,
                UserPoolId=self.user_pool_id,
            )

            for group in groupResponse.get('Groups'):
                user.groups.append(GROUPS(group.get('GroupName')))

            return user
        except ClientError as e:
            error_code = e.response.get('Error').get('Code')
            if error_code == 'NotAuthorizedException':
                raise InvalidTokenError(message="Token inválido ou expirado")
            else:
                raise ForbiddenAction(message=e.response.get('Error').get('Message'))