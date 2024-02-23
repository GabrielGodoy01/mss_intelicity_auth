from src.modules.update_user.app.update_user_viewmodel import UpdateUserViewmodel, UserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE


class Test_UpdateUserViewmodel:

    def test_user_viewmodel(self):
        viewmodel = UserViewmodel(User(role=ROLE.INTELICITY,
                name='Gabriel Godoy',
                email='teste@gmail.com',
                groups=[],))
        
        expected = {
            'name': 'Gabriel Godoy',
            'role': 'INTELICITY',
            'email': 'teste@gmail.com',
            'groups': [],
        }

        assert viewmodel.to_dict() == expected
    
    def test_update_user_viewmodel(self):
        viewmodel = UpdateUserViewmodel(
            
                User(role=ROLE.INTELICITY,
                name='Gabriel Godoy',
                email='teste@gmail.com',
                groups=[],)
            )
        
        expected = {
            'user': {
                'name': 'Gabriel Godoy',
                'role': 'INTELICITY',
                'email': 'teste@gmail.com',
                'groups': [],
                },
            'message': 'Usuário foi atualizado com sucesso!'
        }
    
        assert viewmodel.to_dict() == expected