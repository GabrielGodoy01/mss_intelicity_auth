import enum
from enum import Enum
import os

from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.infra.repositories.user_repository_cognito import UserRepositoryCognito
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

class STAGE(Enum):
    DEV = "DEV"
    HOMOLOG = "HOMOLOG"
    PROD = "PROD"
    TEST = "TEST"


class Environments:
    """
    Defines the environment variables for the application. You should not instantiate this class directly. Please use Environments.get_envs() method instead.

    Usage:

    """
    stage: STAGE

    def load_envs(self):
        if "STAGE" not in os.environ or os.environ["STAGE"] == STAGE.DEV.value:
            os.environ["STAGE"] = os.environ.get("STAGE") or STAGE.DEV.value

        self.stage = STAGE[os.environ.get("STAGE")]

    @staticmethod
    def get_user_repo() -> IUserRepository:
        if Environments.get_envs().stage == STAGE.PROD:
            return UserRepositoryCognito
        else:
            return UserRepositoryMock

    @staticmethod
    def get_envs() -> "Environments":
        """
        Returns the Environments object. This method should be used to get the Environments object instead of instantiating it directly.
        :return: Environments (stage={self.stage})

        """
        envs = Environments()
        envs.load_envs()
        return envs

    def __repr__(self):
        return self.__dict__

