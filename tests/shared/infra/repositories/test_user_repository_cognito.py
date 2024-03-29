import pytest
from src.shared.domain.enums.groups_enum import GROUPS
from src.shared.infra.repositories.user_repository_cognito import UserRepositoryCognito


class Test_UserRepositoryCognito:
    @pytest.mark.skip("Can't test it locally")
    def test_check_token(self):
        repo = UserRepositoryCognito()
        repo.check_token("eyJraWQiOiJ5WUpLc1BCMHh4RHQ5K1VHdTJhR0xCTEpneVwvSFdBZXFDcGF2Z1JIRkpWND0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIxMjVmYjM0ZS1hYWNmLTRhNDctOTkxNC04MmVhNjRmZjlmMzIiLCJjb2duaXRvOmdyb3VwcyI6WyJHQUlBIl0sImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5zYS1lYXN0LTEuYW1hem9uYXdzLmNvbVwvc2EtZWFzdC0xX0N4V0V2RWR6QiIsImNsaWVudF9pZCI6IjJtZ2ZqdTBsNnIyN2FvNjVnOTk4NjZ2dm45Iiwib3JpZ2luX2p0aSI6Ijg0OWJlMmI1LTFhYmEtNDAyZS04MDNlLTYwMDc0NjJkYWM4ZiIsImV2ZW50X2lkIjoiZTdlZGY5MmItZTA4Yi00YjdhLTgzZjktZTEzM2M5NWFkY2RhIiwidG9rZW5fdXNlIjoiYWNjZXNzIiwic2NvcGUiOiJhd3MuY29nbml0by5zaWduaW4udXNlci5hZG1pbiIsImF1dGhfdGltZSI6MTcwNzkzNTg0OSwiZXhwIjoxNzA4OTYyMjg4LCJpYXQiOjE3MDg5NTg2ODgsImp0aSI6IjI3NWIwNzE0LWY5ZWQtNDQyOS1iNDEzLTNkMjYxN2ZhNWFiZiIsInVzZXJuYW1lIjoiMTI1ZmIzNGUtYWFjZi00YTQ3LTk5MTQtODJlYTY0ZmY5ZjMyIn0.LX0fj6w23Xt7tnC8eiXcBp7MQHIMRhHl0l_ph4gzDaoBFoMUdlOKKjIDxyetZYDzLwE_UZz4Gb7nvSs8E3UqeQxhPw2uxWn1G7qgPfu3KY6BVg39UOA922jP_WyhNwd2qr7POpx30DtAonWs6HnzphgXgPo0DjPXo8lQFYMtp59J4630jzujuytZLqty7xAx3baCZnwW4yAWAOd_fjJpKaLqync3XYjs9-l3uTkqhYiQiYfUeNjurNUzdpUzixSfH2O0nxgooylKfyAs2eBVJpDCxowFjx7afqsbb4VTlevo0LPElhePB4QSOX43HjPk15pRUt_uT9rgXmTKUkRJHQ")

    @pytest.mark.skip("Can't test it locally")
    def test_list_groups(self):
        repo = UserRepositoryCognito()
        repo.get_users_in_group(GROUPS.GAIA)

    @pytest.mark.skip("Can't test it locally")
    def test_get_user_by_email(self):
        repo = UserRepositoryCognito()
        repo.get_user_by_email("teste1234@gmail.com")