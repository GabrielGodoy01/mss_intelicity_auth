from .check_token_controller import CheckTokenController
from .check_token_usecase import CheckTokenUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo = Environments.get_user_repo()()
usecase = CheckTokenUsecase(repo)
controller = CheckTokenController(usecase)


def update_user_presenter(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()

def lambda_handler(event, context):
    response = update_user_presenter(event, context)
    
    return response

