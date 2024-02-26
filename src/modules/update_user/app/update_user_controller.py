from .update_user_usecase import UpdateUserUsecase
from update_user_viewmodel import UpdateUserViewmodel
from src.shared.domain.enums.groups_enum import GROUPS
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import InvalidCredentials, NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError


class UpdateUserController:

    def __init__(self, usecase: UpdateUserUsecase):
        self.UpdateUserUsecase = usecase
        self.mutable_fields = ['name', 'role']
    
    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('Authorization') is None:
                raise MissingParameters('Authorization header')
            
            token = request.data.get('Authorization').split(' ')

            if len(token) != 2 or token[0] != 'Bearer':
                raise EntityError('Token')
            access_token = token[1]

            if request.data.get('email') is None:
                raise MissingParameters('email')

            if request.data.get('groups') is None:
                raise MissingParameters('groups')
            
            for group in request.data.get('groups'):
                if group not in [g.value for g in GROUPS]:
                    raise EntityError('groups')
            
            groups_enum_list = [GROUPS[group_string] for group_string in request.data.get('groups')]


            user_data = {k: v for k, v in request.data.items() if k in self.mutable_fields}

            user = self.UpdateUserUsecase(
                new_user_data=user_data,
                user_email=request.data.get('email').lower(),
                access_token=access_token,
                groups=groups_enum_list
            )

            viewmodel = UpdateUserViewmodel(user)
            return OK(viewmodel.to_dict())
        
        except MissingParameters as err:
            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except InvalidCredentials as err:
            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except EntityError as err:
            return BadRequest(body=f"Parâmetro inválido: {err.message}")
        
        except NoItemsFound as err:
            return BadRequest(body=err.message)
        
        except Exception as err:
            return InternalServerError(body=err.args[0])