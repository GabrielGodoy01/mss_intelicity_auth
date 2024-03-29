from typing import List
from src.shared.domain.entities.user import User
from src.shared.domain.enums.groups_enum import GROUPS
from src.shared.domain.enums.role_enum import ROLE


class UserViewmodel:
    user_id: str
    name: str
    email: str
    role: ROLE
    groups: List[GROUPS]

    def __init__(self, user: User):
        self.user_id = user.user_id
        self.name = user.name
        self.email = user.email
        self.role = user.role
        self.groups = user.groups

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'role': self.role.value,
            'groups': [group.value for group in self.groups]
        }

class UpdateUserViewmodel:
    user: UserViewmodel

    def __init__(self, user: User):
        self.user = UserViewmodel(user)

    def to_dict(self):
        return {
            'user': self.user.to_dict(),
            'message': 'Usuário foi atualizado com sucesso!'
        }