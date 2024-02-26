from typing import List
from src.shared.domain.entities.user import User
from src.shared.domain.enums.groups_enum import GROUPS
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound


class ListUsersInGroupUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, group: GROUPS, access_token: str) -> List[User]:
            
        user_requester = self.repo.check_token(access_token)

        if user_requester is None:
            raise NoItemsFound("Usuário não encontrado")
        
        if user_requester.role != ROLE.INTELICITY and user_requester.role != ROLE.ADMIN:
            raise ForbiddenAction("user")

        if group not in user_requester.groups:
            raise ForbiddenAction("user não esta no grupo informado")

        users_response = self.repo.get_users_in_group(group=group)

        return users_response