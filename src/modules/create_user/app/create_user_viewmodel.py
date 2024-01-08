from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE


class UserViewmodel:
    name: str
    email: str
    role: ROLE

    def __init__(self, user: User):
        self.user_id = user.user_id
        self.name = user.name
        self.email = user.email
        self.ra = user.ra
        self.role = user.role
        self.access_level = user.access_level
        self.social_name = user.social_name
        self.phone = user.phone

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'role': self.role.value,
        }


class CreateUserViewmodel:
    user: UserViewmodel

    def __init__(self, user: User):
        self.user = UserViewmodel(user)

    def to_dict(self):
        return {
            'user': self.user.to_dict(),
            'message': 'the user was created'
        }
