from src.modules.update_user.app.update_user_controller import UpdateUserController
from src.modules.update_user.app.update_user_usecase import UpdateUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UpdateUserController:

    def test_update_user_controller(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo)
        controller = UpdateUserController(usecase)
        header = {"Authorization": "Bearer valid_access_token-teste@gmail.com"}

        request = HttpRequest(body={
            'name': 'Gabriel Godoy',
            'email': 'teste@gmail.com',
            'role': 'USER',
            'groups': ['GAIA']
        }, headers=header)

        response = controller(request)

        assert response.status_code == 200
        assert response.body == {
            'user': {
                'user_id': '1',
                'name': 'Gabriel Godoy',
                'role': 'USER',
                'email': 'teste@gmail.com',
                'groups': ['GAIA']
            }, 
            'message': 'Usuário foi atualizado com sucesso!'
        }
    
    def test_update_user_controller_no_authorization_header(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo)
        controller = UpdateUserController(usecase)

        request = HttpRequest(body={
            'name': 'Gabriel Godoy',
            'email': 'teste@gmail.com',
            'role': 'USER',
            'groups': ['GAIA']
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Parâmetro ausente: Authorization header"
    
    def test_update_user_controller_authorization_header_not_bearer(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo)
        controller = UpdateUserController(usecase)
        header = {"Authorization": "valid_access_token-teste@gmail.com"}

        request = HttpRequest(body={
            'name': 'Gabriel Godoy',
            'email': 'teste@gmail.com',
            'role': 'USER',
            'groups': ['GAIA']
        }, headers=header)

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Parâmetro inválido: Token"
    
    def test_update_user_controller_no_email(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo)
        controller = UpdateUserController(usecase)
        header = {"Authorization": "Bearer valid_access_token-teste@gmail.com"}

        request = HttpRequest(body={
            'name': 'Gabriel Godoy',
            'role': 'USER',
            'groups': ['GAIA']
        }, headers=header)

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Parâmetro ausente: email"
    
    def test_update_user_controller_no_groups(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo)
        controller = UpdateUserController(usecase)
        header = {"Authorization": "Bearer valid_access_token-teste@gmail.com"}

        request = HttpRequest(body={
            'name': 'Gabriel Godoy',
            'role': 'USER',
            'email': 'teste@gmail.com',
        }, headers=header)

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Parâmetro ausente: groups"
    
    def test_update_user_controller_groups_not_set(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo)
        controller = UpdateUserController(usecase)
        header = {"Authorization": "Bearer valid_access_token-teste@gmail.com"}

        request = HttpRequest(body={
            'name': 'Gabriel Godoy',
            'role': 'USER',
            'email': 'teste@gmail.com',
            'groups': ['123']
        }, headers=header)

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Parâmetro inválido: groups"