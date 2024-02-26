from enum import Enum
from typing import List, Optional
from src.shared.domain.entities.user import User
from src.shared.domain.enums.groups_enum import GROUPS
from src.shared.domain.enums.role_enum import ROLE


class UserCognitoDTO:
    name: str
    email: str
    role: ROLE
    groups: List[GROUPS]

    def __init__(self, email: str, name: str, role: ROLE, groups: List[GROUPS] = []):
        self.email = email
        self.name = name
        self.role = role
        self.groups = groups

    @staticmethod
    def from_entity(user: User):
        return UserCognitoDTO(
            email=user.email,
            name=user.name,
            role=user.role,
            groups=user.groups
        )

    TO_COGNITO_DICT = {
        "email": "email",
        "name": "name",
        "role": "custom:general_role",
    }

    def to_cognito_attributes(self) -> List[dict]:
        user_attributes = [self.parse_attribute(value=getattr(self, att), name=self.TO_COGNITO_DICT[att]) for att in self.TO_COGNITO_DICT]
        user_attributes = [att for att in user_attributes if att["Value"] != str(None)]

        return user_attributes

    FROM_COGNITO_DICT = {value: key for key, value in TO_COGNITO_DICT.items()}
    
    @staticmethod
    def from_cognito(data: dict) -> "UserCognitoDTO":
        user_data = next((value for key, value in data.items() if "Attribute" in key), None)

        user_data = {UserCognitoDTO.FROM_COGNITO_DICT[att["Name"]]: att["Value"] for att in user_data if att["Name"] in UserCognitoDTO.FROM_COGNITO_DICT}
        # user_data["created_at"] = data.get("UserCreateDate")
        # user_data["updated_at"] = data.get("UserLastModifiedDate")
        # user_data["enabled"] = f'{data.get("Enabled")}'
        # user_data["status"] = f'{data.get("UserStatus")}'

        return UserCognitoDTO(
            email=str(user_data["email"]),
            name=str(user_data["name"]),
            role = ROLE[user_data.get("role")],
        )

    def to_entity(self) -> User:
        return User(
            email=self.email,
            name=self.name,
            role=self.role,
            groups=self.groups
        )
    
    @staticmethod
    def parse_attribute(name, value) -> dict:
        return {'Name': name, 'Value': str(value)}


