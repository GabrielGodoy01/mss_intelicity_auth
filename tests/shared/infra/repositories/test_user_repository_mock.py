from src.shared.domain.entities.user import User
from src.shared.domain.enums.groups_enum import GROUPS
from src.shared.domain.enums.role_enum import ROLE
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
import pytest


class Test_UserRepositoryMock:
    def test_get_user_by_email(self):
        repo = UserRepositoryMock()
        user = repo.get_user_by_email('teste@gmail.com')

        assert user.name == 'Gabriel Godoy'
        assert type(user) == User

    def test_create_user(self):
        repo = UserRepositoryMock()
        user = repo.create_user(
            new_user=User(email='teste3@gmail.com', name='Gabriel Godoy', role=ROLE.INTELICITY))

        assert len(repo.users) == 4
        assert type(user) == User
        assert repo.users[-1] == user

    def test_check_token(self):
        repo = UserRepositoryMock()
        user = repo.check_token(token="valid_access_token-teste@gmail.com")
        assert user.email == 'teste@gmail.com'
        assert type(user) == User
        assert user.name == 'Gabriel Godoy'
        assert user.role == ROLE.INTELICITY
        assert user.groups == [GROUPS.GAIA]

    def test_get_users_in_group(self):
        repo = UserRepositoryMock()
        users = repo.get_users_in_group(GROUPS.GAIA)

        assert len(users) == 1
        assert type(users[0]) == User
        assert users[0].email == 'teste@gmail.com'
        assert users[0].name == 'Gabriel Godoy'
        assert users[0].role == ROLE.INTELICITY
        assert users[0].groups == [GROUPS.GAIA]
    
    def test_update_user(self):
        repo = UserRepositoryMock()
        user = repo.update_user(user_email='teste@gmail.com', kvp_to_update={'role': ROLE.USER}, addGroups=[GROUPS.TEST], removeGroups=[GROUPS.GAIA])

        assert user.email == 'teste@gmail.com'
        assert type(user) == User
        assert user.role == ROLE.USER
        assert user.groups == [GROUPS.TEST]