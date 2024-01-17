from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateUseUsecase:

    def test_create_user_usecase(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        user = User(role=ROLE.INTELICITY,
            name='Gabriel Godoy',
            email='teste@gmail.com',
            groups=[],)
        
        user_response = usecase(user)

        assert user_response.role == ROLE.INTELICITY
        