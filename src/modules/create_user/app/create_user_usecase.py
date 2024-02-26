from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound


class CreateUserUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user_to_create: User, access_token: str) -> User:

        user_requester = self.repo.check_token(access_token)

        if user_requester is None:
            raise NoItemsFound("Usuário não encontrado")
        
        if user_requester.role != ROLE.INTELICITY and user_requester.role != ROLE.ADMIN:
            raise ForbiddenAction("user")

        user_to_create.email = user_to_create.email.lower()
        
        user_response = self.repo.create_user(user_to_create)

        return user_response
