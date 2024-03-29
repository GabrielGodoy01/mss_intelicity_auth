import datetime
import json
from src.shared.domain.enums.groups_enum import GROUPS
from src.shared.domain.enums.role_enum import ROLE
from .create_user_viewmodel import CreateUserViewmodel
from src.shared.domain.entities.user import User
from .create_user_usecase import CreateUserUsecase
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, InvalidCredentials, InvalidTokenError, NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import BadRequest, InternalServerError, Conflict, \
    Created, Forbidden, Unauthorized


class CreateUserController:
    def __init__(self, usecase: CreateUserUsecase) -> None:
        self.createUserUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            
            if request.data.get('Authorization') is None:
                raise MissingParameters('Authorization header')

            token = request.data.get('Authorization').split(' ')

            if len(token) != 2 or token[0] != 'Bearer':
                raise EntityError('Token')
            access_token = token[1]

            if request.data.get('role') is None:
                raise MissingParameters('role')

            if request.data.get('role') not in [role.value for role in ROLE]:
                raise EntityError('role')

            if request.data.get('name') is None:
                raise MissingParameters('name')

            if request.data.get('email') is None:
                raise MissingParameters('email')

            if request.data.get('groups') is None:
                raise MissingParameters('groups')
                        
            for group in request.data.get('groups'):
                if group not in [g.value for g in GROUPS]:
                    raise EntityError(f'groups')

            user_dict = {
                'email': request.data.get('email').replace(' ', ''),
                'name': request.data.get('name'),
                'role': request.data.get('role'),
                'groups': request.data.get('groups'),
            }

            new_user = User.parse_object(user_dict)
            created_user = self.createUserUsecase(user_to_create=new_user, access_token=access_token)
            viewmodel = CreateUserViewmodel(created_user)
            response = Created(viewmodel.to_dict())
            
            return response

        except DuplicatedItem as err:
            return Conflict(body=f"Usuário ja cadastrado com esses dados")

        except MissingParameters as err:
            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except InvalidCredentials as err:
            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except EntityError as err:
            return BadRequest(body=f"Parâmetro inválido: {err.message}")
        
        except NoItemsFound as err:
            return BadRequest(body=err.message)
        
        except InvalidTokenError as err:
            return Unauthorized(body="Token inválido ou expirado")
        
        except Exception as err:
            return InternalServerError(body=err.args[0])
