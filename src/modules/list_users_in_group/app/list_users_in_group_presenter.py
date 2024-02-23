from src.modules.list_users_in_group.app.list_users_in_group_controller import ListUsersInGroupController
from src.modules.list_users_in_group.app.list_users_in_group_usecase import ListUsersInGroupUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse


repo = Environments.get_user_repo()()
usecase = ListUsersInGroupUsecase(repo)
controller = ListUsersInGroupController(usecase)

def lambda_handler(event, context):
    
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    
    return httpResponse.toDict()