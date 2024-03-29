from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .refresh_token_controller import RefreshTokenController
from .refresh_token_usecase import RefreshTokenUsecase
from src.shared.environments import Environments


repo = Environments.get_user_repo()()
usecase = RefreshTokenUsecase(repo)
controller = RefreshTokenController(usecase)

def lambda_handler(event, context):
    
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    
    return httpResponse.toDict()