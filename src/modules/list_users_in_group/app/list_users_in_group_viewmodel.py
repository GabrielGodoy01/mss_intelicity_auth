from typing import List
from src.shared.domain.entities.user import User
from src.shared.domain.enums.groups_enum import GROUPS
from src.shared.domain.enums.role_enum import ROLE


class UserViewmodel:
    name: str
    email: str
    role: ROLE
    groups: List[GROUPS]

    def __init__(self, user: User):
        self.name = user.name
        self.email = user.email
        self.role = user.role
        self.groups = user.groups

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'role': self.role.value,
            'groups': [group.value for group in self.groups]
        }

class ListUsersInGroupViewmodel:
    users: List[UserViewmodel]

    def __init__(self, users: List[User]):
        self.users = [UserViewmodel(user).to_dict() for user in users]

    def to_dict(self):
        return {
            'users': self.users,
            'message': 'Usuários foram listados com sucesso!'
        }