from src.modules.check_token.app.check_token_viewmodel import CheckTokenViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE


class Test_CheckTokenViewmodel:

    def test_check_token_viewmodel(self):
        viewmodel = CheckTokenViewmodel(
            user=User(role=ROLE.INTELICITY,
            name='Gabriel Godoy',
            email='teste@gmail.com',
            groups=[],)
        )

        expected = {
            'user': {
                'name': 'Gabriel Godoy',
                'role': 'INTELICITY',
                'email': 'teste@gmail.com',
                'valid_token': True,
                'groups': []
            },
            'message': 'Token de usuário válido!'
        }

        assert viewmodel.to_dict() == expected