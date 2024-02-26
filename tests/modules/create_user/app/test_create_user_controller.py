from src.modules.create_user.app.create_user_controller import CreateUserController
from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateUserController:

    def test_create_user_controller(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        controller = CreateUserController(usecase)
        header = {"Authorization": "Bearer valid_access_token-teste@gmail.com"}

        request = HttpRequest(body={
            'name': 'Gabriel Godoy',
            'email': 'teste@gmail.com',
            'role': 'INTELICITY',
            'groups': ['GAIA']
        }, headers=header)

        response = controller(request)

        assert response.status_code == 201
        assert response.body == {
            'user': {
                'name': 'Gabriel Godoy',
                'role': 'INTELICITY',
                'email': 'teste@gmail.com',
                'groups': ['GAIA']
            }, 
            'message': 'Usuário foi criado com sucesso!'
        }
    
    def test_create_user_controller_no_authorization_header(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        controller = CreateUserController(usecase)

        request = HttpRequest(body={
            'name': 'Gabriel Godoy',
            'email': 'teste@gmail.com',
            'groups': ['GAIA']
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Parâmetro ausente: Authorization header"
    
    def test_create_user_controller_authorization_header_not_bearer(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        controller = CreateUserController(usecase)
        header = {"Authorization": "valid_access_token-teste@gmail.com"}

        request = HttpRequest(body={
            'name': 'Gabriel Godoy',
            'email': 'teste@gmail.com',
            'groups': ['GAIA']
        }, headers=header)

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Parâmetro inválido: Token"
    
    def test_create_user_controller_no_role(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        controller = CreateUserController(usecase)
        header = {"Authorization": "Bearer valid_access_token-teste@gmail.com"}

        request = HttpRequest(body={
            'name': 'Gabriel Godoy',
            'email': 'teste@gmail.com',
            'groups': ['GAIA']
        }, headers=header)

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Parâmetro ausente: role"
    
    def test_create_user_controller_role_not_valid(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        controller = CreateUserController(usecase)
        header = {"Authorization": "Bearer valid_access_token-teste@gmail.com"}

        request = HttpRequest(body={
            'name': 'Gabriel Godoy',
            'role': '123',
            'email': 'teste@gmail.com',
            'groups': ['GAIA']
        }, headers=header)

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Parâmetro inválido: role"

    
    def test_create_user_controller_no_name(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        controller = CreateUserController(usecase)
        header = {"Authorization": "Bearer valid_access_token-teste@gmail.com"}


        request = HttpRequest(body={
            'email': 'teste@gmail.com',
            'role': 'INTELICITY',
            'groups': ['GAIA']
        }, headers=header)

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Parâmetro ausente: name"
    
    def test_create_user_controller_no_email(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        controller = CreateUserController(usecase)
        header = {"Authorization": "Bearer valid_access_token-teste@gmail.com"}

        request = HttpRequest(body={
            'name': 'Gabriel Godoy',
            'role': 'INTELICITY',
            'groups': ['GAIA']
        }, headers=header)

        response = controller(request)

        assert response.status_code == 400
    
    def test_create_user_controller_no_groups(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        controller = CreateUserController(usecase)
        header = {"Authorization": "Bearer valid_access_token-teste@gmail.com"}

        request = HttpRequest(body={
            'name': 'Gabriel Godoy',
            'email': 'teste@gmail.com',
            'role': 'INTELICITY',
        }, headers=header)

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Parâmetro ausente: groups"
