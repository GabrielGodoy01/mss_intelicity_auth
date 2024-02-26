import pytest

from src.modules.check_token.app.check_token_usecase import CheckTokenUsecase
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CheckTokenUsecase:

    def test_check_token_usecase(self):
        repo = UserRepositoryMock()
        usecase = CheckTokenUsecase(repo)

        email = 'teste@gmail.com'
        access_token = f'valid_access_token-{email}'

        user = usecase(access_token)

        assert user.role == ROLE.INTELICITY

    def test_check_token_usecase_invalid_email(self):
        repo = UserRepositoryMock()
        usecase = CheckTokenUsecase(repo)

        invalid_email = 'etset@gmail.com'
        access_token = f'valid_access_token-{invalid_email}'

        with pytest.raises(NoItemsFound):
            usecase(access_token)