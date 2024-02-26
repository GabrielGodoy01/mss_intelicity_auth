from typing import List
from src.shared.domain.entities.user import User
from src.shared.domain.enums.groups_enum import GROUPS
from src.shared.domain.enums.role_enum import ROLE

class UserViewmodel:
    user_id: str
    email: str
    name: str
    role: ROLE
    groups: List[GROUPS]

    def __init__(self, user_id: str, email: str, name: str, role: ROLE, groups: List[GROUPS]):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.role = role
        self.groups = groups
       

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'email': self.email,
            'name': self.name,
            'role': self.role.value,
            'groups': [group.value for group in self.groups],
            'valid_token': True
        }

class CheckTokenViewmodel():
    user: UserViewmodel

    def __init__(self, user: User):
        self.user = UserViewmodel(user_id=user.user_id, email=user.email,name=user.name, role=user.role, groups=user.groups)

    def to_dict(self):
        return {
            'user': self.user.to_dict(),
            'message': 'Token de usuário válido!'
        }
