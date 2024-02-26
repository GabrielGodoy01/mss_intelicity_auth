from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound


class CheckTokenUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, token: str) -> User:

        user = self.repo.check_token(token)

        if not user:
            raise NoItemsFound('Usuário não encontrado')

        return user
