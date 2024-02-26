from src.modules.create_user.app.create_user_viewmodel import CreateUserViewmodel, UserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE


class Test_CreateUserViewmodel:

    def test_check_token_viewmodel(self):
        viewmodel = CreateUserViewmodel(
            user=User(user_id="123",role=ROLE.INTELICITY,
            name='Gabriel Godoy',
            email='teste@gmail.com',
            groups=[],)
        )

        expected = {
            'user': {
                'user_id': '123',
                'name': 'Gabriel Godoy',
                'role': 'INTELICITY',
                'email': 'teste@gmail.com',
                'groups': []
            },
            'message': 'Usuário foi criado com sucesso!'
        }

        assert viewmodel.to_dict() == expected

    def test_user_viewmodel(self):
        viewmodel = UserViewmodel(User(user_id="123",role=ROLE.INTELICITY,
                name='Gabriel Godoy',
                email='teste@gmail.com',
                groups=[],))
        
        expected = {
            'user_id': '123',
            'name': 'Gabriel Godoy',
            'role': 'INTELICITY',
            'email': 'teste@gmail.com',
            'groups': [],
        }

        assert viewmodel.to_dict() == expected