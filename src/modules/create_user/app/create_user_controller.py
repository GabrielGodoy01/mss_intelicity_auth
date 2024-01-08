import datetime
import json
from src.shared.domain.enums.role_enum import ROLE
from .create_user_viewmodel import CreateUserViewmodel
from src.shared.domain.entities.user import User
from .create_user_usecase import CreateUserUsecase
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, InvalidCredentials, InvalidAdminError, \
    InvalidProfessorError, InvalidStudentError, TermsNotAcceptedError
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import BadRequest, InternalServerError, Conflict, \
    Created, Forbidden


class CreateUserController:
    def __init__(self, usecase: CreateUserUsecase) -> None:
        self.createUserUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:

            if request.data.get('role') is None:
                raise MissingParameters('role')

            if request.data.get('role') not in [role.value for role in ROLE]:
                raise EntityError('role')

            if request.data.get('name') is None:
                raise MissingParameters('name')

            if request.data.get('email') is None:
                raise MissingParameters('email')

            user_dict = {
                'email': request.data.get('email').replace(' ', ''),
                'name': request.data.get('name'),
                'role': request.data.get('role'),
                'groups': request.data.get('groups'),
            }

            new_user = User.parse_object(user_dict)
            created_user = self.createUserUsecase(new_user)

            viewmodel = CreateUserViewmodel(created_user)
            response = Created(viewmodel.to_dict())
            self.observability.log_controller_out(input=json.dumps(response.body), status_code=response.status_code)
            
            return response

        except DuplicatedItem as err:
            self.observability.log_exception(status_code=409, exception_name="DuplicatedItem", message=err.message)
            return Conflict(body=f"Usuário ja cadastrado com esses dados: {err.message}" if err.message != "user" else "Usuário ja cadastrado com esses dados")

        except InvalidProfessorError as err:
            self.observability.log_exception(status_code=400, exception_name="InvalidProfessorError", message=err.message)
            return BadRequest(body=f"Apenas professores do Instituto Mauá de Tecnologia podem se cadastrar com o nível de acesso professor")

        except MissingParameters as err:
            self.observability.log_exception(status_code=400, exception_name="MissingParameters", message=err.message)

            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except InvalidCredentials as err:
            self.observability.log_exception(status_code=400, exception_name="InvalidCredentials", message=err.message)
            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except EntityError as err:
            self.observability.log_exception(status_code=400, exception_name="EntityError", message=err.message)

            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except InvalidAdminError as err:
            self.observability.log_exception(status_code=403, exception_name="InvalidAdminError", message=err.message)
            return Forbidden(body="Impossível criar usuário com nível de acesso ADMIN")

        except InvalidStudentError as err:
            self.observability.log_exception(status_code=400, exception_name="InvalidStudentError", message=err.message)
            return BadRequest(body="Estudante necessita de RA válido")

        except TermsNotAcceptedError as err:
            self.observability.log_exception(status_code=400, exception_name="TermsNotAcceptedError", message=err.message)
            return BadRequest(body="É necessário aceitar os termos de uso para se cadastrar")

        except Exception as err:
            self.observability.log_exception(status_code=500, exception_name=type(err).__name__, message=err.args[0])

            return InternalServerError(body=err.args[0])
