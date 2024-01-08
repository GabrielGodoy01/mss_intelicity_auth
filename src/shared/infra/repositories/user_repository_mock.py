from typing import List

from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE, STATE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class UserRepositoryMock(IUserRepository):
    users: List[User]
    user_counter: int

    def __init__(self):
        self.users = [
            User(email='teste@gmail.com', name='Gabriel Godoy', role=ROLE.INTELICITY)
        ]

    def create_user(self, new_user: User) -> User:
        self.users.append(new_user)
        self.user_counter += 1
        return new_user
    
    def get_user_by_email(self, email: str) -> User:
        user: User = None
        for userx in self.users:
            if userx.email == email:
                user = userx
                break
            pass
        return user
    
    def check_token(self, token: str) -> dict:

        split_token = token.split("-")
        if len(split_token) != 2 or split_token[0] != "valid_access_token":
            raise EntityError('access_token')

        email = split_token[1]
        user = self.get_user_by_email(email)

        if user is None:
            return None

        data = user.to_dict()
        return data
