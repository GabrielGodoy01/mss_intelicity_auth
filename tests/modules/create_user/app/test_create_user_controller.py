from src.modules.create_user.app.create_user_controller import CreateUserController
from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateUserController:

    def test_create_user_controller(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        controller = CreateUserController(usecase)

        request = HttpRequest(body={
            'name': 'Gabriel Godoy',
            'email': 'teste@gmail.com',
            'role': 'INTELICITY',
            'groups': ['GAIA']
        })

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
    
    def test_create_user_controller_no_role(self):
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
    
    def test_create_user_controller_role_not_valid(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        controller = CreateUserController(usecase)

        request = HttpRequest(body={
            'name': 'Gabriel Godoy',
            'role': '123',
            'email': 'teste@gmail.com',
            'groups': ['GAIA']
        })

        response = controller(request)

        assert response.status_code == 400

    
    def test_create_user_controller_no_name(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        controller = CreateUserController(usecase)

        request = HttpRequest(body={
            'email': 'teste@gmail.com',
            'role': 'INTELICITY',
            'groups': ['GAIA']
        })

        response = controller(request)

        assert response.status_code == 400
    
    def test_create_user_controller_no_email(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        controller = CreateUserController(usecase)

        request = HttpRequest(body={
            'name': 'Gabriel Godoy',
            'role': 'INTELICITY',
            'groups': ['GAIA']
        })

        response = controller(request)

        assert response.status_code == 400
    
    def test_create_user_controller_no_groups(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        controller = CreateUserController(usecase)

        request = HttpRequest(body={
            'name': 'Gabriel Godoy',
            'email': 'teste@gmail.com',
            'role': 'INTELICITY',
        })

        response = controller(request)

        assert response.status_code == 400
