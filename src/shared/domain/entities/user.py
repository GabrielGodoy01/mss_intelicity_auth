import abc
import re
from typing import List

from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.domain_errors import EntityError


class User(abc.ABC):
    name: str
    email: str
    role: ROLE
    groups: List[str]
    MIN_NAME_LENGTH = 2

    def __init__(self, name: str, email: str, role: ROLE, groups: List[str] = []):
        if not User.validate_name(name):
            raise EntityError("name")
        self.name = name

        if not User.validate_email(email):
            raise EntityError("email")
        self.email = email

        if type(role) != ROLE:
            raise EntityError("role")
        self.role = role

        if type(groups) != list:
            raise EntityError("groups")
        self.groups = groups

    @staticmethod
    def parse_object(user: dict) -> 'User':
        return User(
            email=user['email'],
            name=user['name'].title(),
            role=ROLE[user['role']],
            groups=user.get('groups', [])
        )

    @staticmethod
    def validate_name(name: str) -> bool:
        if name is None:
            return False
        elif type(name) != str:
            return False
        elif len(name) < User.MIN_NAME_LENGTH:
            return False

        return True

    @staticmethod
    def validate_email(email: str) -> bool:
        if email is None:
            return False

        regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

        return bool(re.fullmatch(regex, email))



    def __repr__(self):
        return f"User(name={self.name}, email={self.email}, role={self.role})"
