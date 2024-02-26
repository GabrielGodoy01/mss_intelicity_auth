from src.modules.list_users_in_group.app.list_users_in_group_viewmodel import ListUsersInGroupViewmodel, UserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE


class Test_ListUsersInGroupViewmodel:

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
        
    def test_list_users_in_group_viewmodel(self):
        viewmodel = ListUsersInGroupViewmodel(
            users=[
                User(user_id="123",role=ROLE.INTELICITY,
                name='Gabriel Godoy',
                email='teste@gmail.com',
                groups=[],)
            ])
        
        expected = {
            'users': [{
                'user_id': '123',
                'name': 'Gabriel Godoy',
                'role': 'INTELICITY',
                'email': 'teste@gmail.com',
                'groups': [],
                }],
            'message': 'Usuários foram listados com sucesso!'
        }
    
        assert viewmodel.to_dict() == expected
    