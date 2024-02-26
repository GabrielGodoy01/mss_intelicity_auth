from src.modules.list_users_in_group.app.list_users_in_group_controller import ListUsersInGroupController
from src.modules.list_users_in_group.app.list_users_in_group_usecase import ListUsersInGroupUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_ListUsersInGroupController:

    def test_list_users_in_group_controller(self):
        repo = UserRepositoryMock()
        usecase = ListUsersInGroupUsecase(repo)
        controller = ListUsersInGroupController(usecase)
        header = {"Authorization": "Bearer valid_access_token-teste@gmail.com"}

        request = HttpRequest(body={
            'group': 'GAIA'
        }, headers=header)

        response = controller(request)

        assert response.status_code == 200
        assert response.body == {
            'users': [
                {
                    'user_id': '1',
                    'name': 'Gabriel Godoy',
                    'role': 'INTELICITY',
                    'email': 'teste@gmail.com',
                    'groups': ['GAIA']
                }
            ],
            'message': 'Usuários foram listados com sucesso!'
        }