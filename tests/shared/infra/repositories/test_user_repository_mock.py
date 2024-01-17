from src.shared.domain.entities.user import User
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

        assert len(repo.users) == 3
        assert type(user) == User
        assert repo.users[-1] == user

    def test_check_token(self):
        repo = UserRepositoryMock()
        user = repo.check_token(token="valid_access_token-teste@gmail.com")
        assert user.email == 'teste@gmail.com'
        assert type(user) == User
        assert user.name == 'Gabriel Godoy'
        assert user.role == ROLE.INTELICITY
        assert user.groups == []