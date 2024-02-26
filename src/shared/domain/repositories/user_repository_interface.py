from abc import ABC, abstractmethod
from typing import List, Tuple

from src.shared.domain.entities.user import User
from src.shared.domain.enums.groups_enum import GROUPS


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

    @abstractmethod
    def get_users_in_group(self, group: GROUPS) -> List[User]:
        pass

    @abstractmethod
    def update_user(self, user_email: str, kvp_to_update: dict, addGroups: List[GROUPS] = None, removeGroups: List[GROUPS] = None) -> User:
        pass

    @abstractmethod
    def refresh_token(self, refresh_token: str) -> Tuple[str, str, str]:
        pass
