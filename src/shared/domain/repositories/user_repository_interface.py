from abc import ABC, abstractmethod
from typing import List

from src.shared.domain.entities.user import User


class IUserRepository(ABC):

    @abstractmethod
    def create_user(self, new_user: User) -> User:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def check_token(self, token: str) -> User:  # user data
        pass
