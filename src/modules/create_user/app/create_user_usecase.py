from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository


class CreateUserUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user: User) -> User:

        user.email = user.email.lower()
        
        user_response = self.repo.create_user(user)

        return user_response
