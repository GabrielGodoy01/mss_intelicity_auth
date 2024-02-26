import pytest
from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateUseUsecase:

    def test_create_user_usecase(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        user = User(role=ROLE.INTELICITY,
            name='Gabriel Godoy',
            email='teste@gmail3.com',
            groups=[],)
        
        user_response = usecase(user_to_create=user, access_token="valid_access_token-teste@gmail.com")

        assert user_response.role == ROLE.INTELICITY
    
    def test_create_user_usecase_with_invalid_token(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        user = User(role=ROLE.INTELICITY,
            name='Gabriel Godoy',
            email='teste@gmail.com',
            groups=[],)
    
        with pytest.raises(NoItemsFound):
            usecase(user_to_create=user, access_token="valid_access_token-teste3232@gmail.com")
    
    def test_create_user_usecase_with_user_not_admin(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        user = User(
            role=ROLE.INTELICITY,
            name='Gabriel Godoy',
            email='teste@gmail.com',
            groups=[],
        )
    
        with pytest.raises(ForbiddenAction):
            usecase(user_to_create=user, access_token="valid_access_token-teste3@gmail.com")

        