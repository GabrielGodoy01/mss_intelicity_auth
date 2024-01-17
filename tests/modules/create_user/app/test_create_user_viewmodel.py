from src.modules.create_user.app.create_user_viewmodel import CreateUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE


class Test_CreateUserViewmodel:

    def test_check_token_viewmodel(self):
        viewmodel = CreateUserViewmodel(
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
                'groups': []
            },
            'message': 'Usuário foi criado com sucesso!'
        }

        assert viewmodel.to_dict() == expected