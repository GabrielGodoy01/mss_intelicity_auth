from src.modules.check_token.app.check_token_controller import CheckTokenController
from src.modules.check_token.app.check_token_usecase import CheckTokenUsecase
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CheckTokenController:

    def test_check_token_controller(self):
        repo = UserRepositoryMock()
        usecase = CheckTokenUsecase(repo)
        controller = CheckTokenController(usecase)

        header = {"Authorization": "Bearer valid_access_token-teste@gmail.com"}
        request = HttpRequest(headers=header)

        response = controller(request)
        assert response.status_code == 200
        assert response.body == {
            'user': {
                'name': 'Gabriel Godoy',
                'role': 'INTELICITY',
                'email': 'teste@gmail.com',
                'valid_token': True,
                'groups': []
            },
            'message': 'Token de usuário válido!'
        }

    def test_check_token_controller_invalid_token(self):
        repo = UserRepositoryMock()
        usecase = CheckTokenUsecase(repo)
        controller = CheckTokenController(usecase)

        header = {"Authorization": "Bearer INVALID_access_token-teste@gmail.com"}
        request = HttpRequest(headers=header)

        response = controller(request)
        assert response.status_code == 400
        assert response.body["message"] == 'Parâmetro inválido: Campo access_token não é válido'