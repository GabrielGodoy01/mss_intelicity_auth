from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, InvalidCredentials
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import BadRequest, OK, Forbidden, InternalServerError
from .check_token_viewmodel import CheckTokenViewmodel
from .check_token_usecase import CheckTokenUsecase


class CheckTokenController:
    def __init__(self, usecase: CheckTokenUsecase) -> None:
        self.checkTokenUsecase = usecase

    def __call__(self, req: IRequest) -> IResponse:
        try:
            if req.headers.get('Authorization') is None:
                raise MissingParameters('Authorization')
            
            token = req.headers.get('Authorization').split(' ')
            if len(token) != 2 or token[0] != 'Bearer':
                return BadRequest('Token Inválido')
            access_token = token[1]
            user = self.checkTokenUsecase(access_token)
            viewmodel = CheckTokenViewmodel(user)
            return OK(viewmodel.to_dict())
        
        except MissingParameters as err:
            return BadRequest(body={"message": f"Parâmetro ausente: {err.message}"})
        
        except EntityError as err:
            return BadRequest(body={"message": f"Parâmetro inválido: {err.message}"})

        except ForbiddenAction as err:
            return Forbidden(body={"message": f"Ação não permitida: {err.message}"})

        except InvalidCredentials as err:
            return BadRequest(body={"message": f"Token inválido: {err.message}"})

        except Exception as err:
            return InternalServerError(body={"message": err.args[0]})
