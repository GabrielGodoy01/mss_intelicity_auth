from typing import List
from src.shared.domain.entities.user import User
from src.shared.domain.enums.groups_enum import GROUPS
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound


class UpdateUserUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo
        self.immutable_fields = ['email', 'groups']
        self.mutable_fields = ['name', 'role']

    def __call__(self, new_user_data: dict, user_email: str, groups: List[GROUPS], access_token: str) -> User:

        user_requester = self.repo.check_token(access_token)

        if user_requester is None:
            raise NoItemsFound("Usuário não encontrado")
        
        if user_requester.role != ROLE.INTELICITY and user_requester.role != ROLE.ADMIN:
            raise ForbiddenAction("user")

        old_user = self.repo.get_user_by_email(user_email)

        if old_user is None:
            raise NoItemsFound("user")

        old_user_data = User.to_dict(old_user)

        
        kvp_to_update = {k: v for k, v in new_user_data.items() if k in self.mutable_fields and v is not None}

        bool_items = [User.__annotations__[k] for k in self.mutable_fields if User.__annotations__[k] == bool]

        kvp_to_update = {k: eval(v.title()) if User.__annotations__[k] in bool_items and type(v) == str else v for k, v in kvp_to_update.items()}

        for k, v in kvp_to_update.items():
            old_user_data[k] = v if v != "" else None

        kvp_to_update = {k: str(v) for k, v in kvp_to_update.items()}

        add_groups = [group for group in groups if group not in old_user.groups]
        remove_groups = [group for group in old_user.groups if group not in groups]

        user_response = self.repo.update_user(user_email=user_email, kvp_to_update=kvp_to_update, addGroups=add_groups, removeGroups=remove_groups)

        return user_response