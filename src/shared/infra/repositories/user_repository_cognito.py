import json
from typing import Tuple, List

import boto3
from botocore.exceptions import ClientError

from src.shared.domain.entities.user import User
from src.shared.domain.enums.groups_enum import GROUPS
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, ForbiddenAction, InvalidCredentials
from src.shared.infra.dtos.user_cognito_dto import UserCognitoDTO


class UserRepositoryCognito(IUserRepository):

    client: boto3.client
    user_pool_id: str
    client_id: str

    def __init__(self):
        self.client = boto3.client('cognito-idp', region_name=Environments.get_envs().region)
        self.user_pool_id = Environments.get_envs().user_pool_id
        self.client_id = Environments.get_envs().client_id
    
    def get_groups_for_user(self, email: str) -> List[GROUPS]:
        try:
            response = self.client.admin_list_groups_for_user(
                Username=email,
                UserPoolId=self.user_pool_id
            )
            groups = [GROUPS[group.get('GroupName')] for group in response.get('Groups')]
            return groups
        except self.client.exceptions.UserNotFoundException as e:
            raise EntityError(e.response.get('Error').get('Message'))

    
    def get_user_by_email(self, email: str) -> User:
        try:
            response = self.client.admin_get_user(
                UserPoolId=self.user_pool_id,
                Username=email
            )
            if response["UserStatus"] == "UNCONFIRMED":
                return None

            user = UserCognitoDTO.from_cognito(response).to_entity()
            user.groups = self.get_groups_for_user(email)
                
            return user

        except self.client.exceptions.UserNotFoundException:
            return None
    
    def create_user(self, user: User) -> User:
        cognito_attributes = UserCognitoDTO.from_entity(user).to_cognito_attributes()
        try:

            self.client.admin_create_user(
                UserPoolId=self.user_pool_id,
                Username=user.email,
                DesiredDeliveryMediums=["EMAIL"],
                UserAttributes=cognito_attributes)
            
            for group in user.groups:
                self.client.admin_add_user_to_group(
                    UserPoolId=self.user_pool_id,
                    Username=user.email,
                    GroupName=group.value
                )
                
            return user

        except self.client.exceptions.UsernameExistsException:
            raise DuplicatedItem("user")

        except self.client.exceptions.InvalidParameterException as e:
            raise EntityError(e.response.get('Error').get('Message'))
    
    def check_token(self, token: str) -> User:
        try:
            userResponse = self.client.get_user(
                AccessToken=token
            )

            user = UserCognitoDTO.from_cognito(userResponse).to_entity()

            user.groups = self.get_groups_for_user(user.email)
            return user
        except ClientError as e:
            error_code = e.response.get('Error').get('Code')
            if error_code == 'NotAuthorizedException':
                raise InvalidCredentials(message="Token inválido ou expirado")
            else:
                raise ForbiddenAction(message=e.response.get('Error').get('Message'))
    
    def get_users_in_group(self, group: GROUPS) -> List[User]:
        try:
            users = []
            response = self.client.list_users_in_group(
                UserPoolId=self.user_pool_id,
                GroupName=group.value
            )

            for user in response.get('Users'):
                user = UserCognitoDTO.from_cognito(user).to_entity()
                user.groups = [group]
                users.append(user)
            
            return users

        except self.client.exceptions.ResourceNotFoundException as e:
            raise EntityError(e.response.get('Error').get('Message'))

        except self.client.exceptions.InvalidParameterException as e:
            raise EntityError(e.response.get('Error').get('Message'))
    
    def update_user(self, user_email: str, kvp_to_update: dict, addGroups: List[GROUPS] = None, removeGroups: List[GROUPS] = None) -> User:
        try:

            response = self.client.admin_update_user_attributes(
                UserPoolId=self.user_pool_id,
                Username=user_email,
                UserAttributes=[{'Name': UserCognitoDTO.TO_COGNITO_DICT[key], 'Value': value} for key, value in kvp_to_update.items()]
            )

            if addGroups is not None:
                for group in addGroups:
                    self.add_user_to_group(user_email, group)
            
            if removeGroups is not None:
                for group in removeGroups:
                    self.remove_user_from_group(user_email, group)

            user = self.get_user_by_email(user_email)

            return user

        except self.client.exceptions.InvalidParameterException as e:
            raise EntityError(e.response.get('Error').get('Message'))
    
    def add_user_to_group(self, user_email: str, group: GROUPS) -> None:
        try:
            self.client.admin_add_user_to_group(
                UserPoolId=self.user_pool_id,
                Username=user_email,
                GroupName=group.value
            )
        except self.client.exceptions.ResourceNotFoundException as e:
            raise EntityError(e.response.get('Error').get('Message'))

        except self.client.exceptions.InvalidParameterException as e:
            raise EntityError(e.response.get('Error').get('Message'))
    
    def remove_user_from_group(self, user_email: str, group: GROUPS) -> None:
        try:
            self.client.admin_remove_user_from_group(
                UserPoolId=self.user_pool_id,
                Username=user_email,
                GroupName=group.value
            )
        except self.client.exceptions.ResourceNotFoundException as e:
            raise EntityError(e.response.get('Error').get('Message'))

        except self.client.exceptions.InvalidParameterException as e:
            raise EntityError(e.response.get('Error').get('Message'))
    
    def refresh_token(self, refresh_token: str) -> Tuple[str, str, str]:
        try:
            response = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='REFRESH_TOKEN_AUTH',
                AuthParameters={
                    'REFRESH_TOKEN': refresh_token
                }
            )

            id_token = response["AuthenticationResult"]["IdToken"]
            access_token = response["AuthenticationResult"]["AccessToken"]

            return access_token, refresh_token, id_token
        except ClientError as e:
            errorCode = e.response.get('Error').get('Code')
            if errorCode == 'NotAuthorizedException':
                raise InvalidCredentials(message="Token inválido ou expirado")
            else:
                raise ForbiddenAction(message=e.response.get('Error').get('Message'))