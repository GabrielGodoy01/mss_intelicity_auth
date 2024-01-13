import pytest

from src.modules.check_token.app.check_token_usecase import CheckTokenUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CheckTokenUsecase:

    def test_check_token_usecase(self):
        repo = UserRepositoryMock()
        usecase = CheckTokenUsecase(repo)

        email = 'teste@gmail.com'
        access_token = f'valid_access_token-{email}'

        data = usecase(access_token)

        assert data['role'] == 'INTELICITY'

    def test_check_token_usecase_invalid_token(self):
        repo = UserRepositoryMock()
        usecase = CheckTokenUsecase(repo)

        invalid_email = 'etset@gmail.com'
        access_token = f'valid_access_token-{invalid_email}'

        with pytest.raises(ForbiddenAction):
            usecase(access_token)