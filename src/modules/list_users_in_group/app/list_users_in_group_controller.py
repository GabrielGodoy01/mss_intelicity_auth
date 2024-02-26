from src.modules.list_users_in_group.app.list_users_in_group_usecase import ListUsersInGroupUsecase
from src.modules.list_users_in_group.app.list_users_in_group_viewmodel import ListUsersInGroupViewmodel
from src.shared.domain.enums.groups_enum import GROUPS
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import InvalidCredentials, NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError


class ListUsersInGroupController:
    def __init__(self, usecase: ListUsersInGroupUsecase) -> None:
        self.listUsersInGroupUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('Authorization') is None:
                raise MissingParameters('Authorization header')

            token = request.data.get('Authorization').split(' ')

            if len(token) != 2 or token[0] != 'Bearer':
                raise EntityError('Token')
            access_token = token[1]

            if request.data.get('group') is None:
                raise MissingParameters('group')

            if request.data.get('group') not in [g.value for g in GROUPS]:
                    raise EntityError('group')
            
            list_users = self.listUsersInGroupUsecase(group=request.data.get('group'), access_token=access_token)

            viewmodel = ListUsersInGroupViewmodel(users=list_users)

            return OK(viewmodel.to_dict())

        except MissingParameters as err:
            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except InvalidCredentials as err:
            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except EntityError as err:
            return BadRequest(body=f"Parâmetro inválido: {err.message}")
        
        except NoItemsFound as err:
            return BadRequest(body=f"Usuário não encontrado: {err.message}")
        
        except Exception as err:
            return InternalServerError(body=err.args[0])