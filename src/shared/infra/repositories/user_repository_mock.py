from typing import List, Tuple

from src.shared.domain.entities.user import User
from src.shared.domain.enums.groups_enum import GROUPS
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class UserRepositoryMock(IUserRepository):
    users: List[User]

    def __init__(self):
        self.users = [
            User(user_id="1", email='teste@gmail.com', name='Gabriel Godoy', role=ROLE.INTELICITY, groups=[GROUPS.GAIA]),
            User(user_id="2", email='teste2@gmail.com', name='Gabriel Godoy', role=ROLE.INTELICITY),
            User(user_id="3",email='teste3@gmail.com', name='Gabriel Godoy', role=ROLE.USER),
        ]

    def create_user(self, new_user: User) -> User:
        new_user.user_id = str(len(self.users) + 1)
        self.users.append(new_user)
        return self.get_user_by_email(new_user.email)
    
    def get_user_by_email(self, email: str) -> User:
        for userx in self.users:
            if userx.email == email:
                return userx
                
        return None
    
    def check_token(self, token: str) -> User:

        split_token = token.split("-")
        if len(split_token) != 2 or split_token[0] != "valid_access_token":
            raise EntityError('access_token')

        email = split_token[1]
        user = self.get_user_by_email(email)

        if user is None:
            return None

        return user
    
    def get_users_in_group(self, group: GROUPS) -> List[User]:
        users: List[User] = []
        for user in self.users:
            if group in user.groups:
                users.append(user)
        return users
    
    def update_user(self, user_email: str, kvp_to_update: dict, addGroups: List[GROUPS] = None, removeGroups: List[GROUPS] = None) -> User:
        for idx, userx in enumerate(self.users):
            if userx.email == user_email:
                for key, value in kvp_to_update.items():
                    setattr(userx, key, value)
                if addGroups is not None:
                    for group in addGroups:
                        userx.groups.append(group)
                
                if removeGroups is not None:
                    for group in removeGroups:
                        userx.groups.remove(group)
                
                if type(userx.role) == str:
                    userx.role = ROLE[userx.role]

                return userx

        return None

    def refresh_token(self, refresh_token: str) -> Tuple[str, str, str]:
        split_token = refresh_token.split("-")  # token, email
        if len(split_token) != 2:
            return None, None
        if split_token[0] != "valid_refresh_token":
            return None, None
        if self.get_user_by_email(split_token[1]) is None:
            return None, None
        tokens = "valid_access_token-" + split_token[1], refresh_token, "valid_id_token-" + split_token[1]
        return tokens