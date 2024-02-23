import pytest
from src.modules.list_users_in_group.app.list_users_in_group_usecase import ListUsersInGroupUsecase
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_ListUsersInGroupUsecase:

    def test_list_users_in_group_usecase(self):
        repo = UserRepositoryMock()
        usecase = ListUsersInGroupUsecase(repo)
        users_response = usecase(group_name="GAIA", access_token="valid_access_token-teste@gmail.com")

        assert len(users_response) == 1
    
    def test_list_users_in_group_usecase_with_invalid_token(self):
        repo = UserRepositoryMock()
        usecase = ListUsersInGroupUsecase(repo)

        with pytest.raises(NoItemsFound):
            usecase(group_name="GAIA", access_token="valid_access_token-teste3232@gmail.com")
    
    def test_list_users_in_group_usecase_with_user_not_admin(self):
        repo = UserRepositoryMock()
        usecase = ListUsersInGroupUsecase(repo)

        with pytest.raises(ForbiddenAction):
            usecase(group_name="GAIA", access_token="valid_access_token-teste3@gmail.com")
    

    def test_list_users_in_group_usecase_with_user_not_in_group(self):
        repo = UserRepositoryMock()
        usecase = ListUsersInGroupUsecase(repo)

        with pytest.raises(ForbiddenAction):
            usecase(group_name="GAIA", access_token="valid_access_token-teste2@gmail.com")