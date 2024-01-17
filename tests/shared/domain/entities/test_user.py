from src.shared.domain.entities.user import User
from src.shared.domain.enums.groups_enum import GROUPS
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.domain_errors import EntityError
import pytest


class Test_User:
    def test_user(self):
        User(name="GODOY", email="teste123@maua.br", role=ROLE.INTELICITY, groups=[GROUPS.GAIA])

    def test_user_name_is_none(self):
        with pytest.raises(EntityError):
            User(name=None, email="teste123@maua.br", role=ROLE.INTELICITY, groups=[GROUPS.GAIA])

    def test_user_name_is_not_str(self):
        with pytest.raises(EntityError):
            User(name=123, email="teste123@maua.br", role=ROLE.INTELICITY, groups=[GROUPS.GAIA])

    def test_user_name_is_shorter_than_min_length(self):
        with pytest.raises(EntityError):
            User(name="G", email="teste123@maua.br", role=ROLE.INTELICITY, groups=[GROUPS.GAIA])

    def test_user_email_is_none(self):
        with pytest.raises(EntityError):
            User(name="GODOY", email=None, role=ROLE.INTELICITY, groups=[GROUPS.GAIA])

    def test_user_email_is_not_valid(self):
        with pytest.raises(EntityError):
            User(name="GODOY", email="teste", role=ROLE.INTELICITY, groups=[GROUPS.GAIA])
    
    def test_user_email_is_not_str(self):
        with pytest.raises(EntityError):
            User(name='123', email=123, role=ROLE.INTELICITY, groups=[GROUPS.GAIA])
    
    def test_user_role_is_none(self):
        with pytest.raises(EntityError):
            User(name='GODOY', email="teste123@maua.br", role=None, groups=[GROUPS.GAIA])

    def test_user_role_is_not_enum(self):
        with pytest.raises(EntityError):
            User(name='GODOY', email="teste123@maua.br", role=123, groups=[GROUPS.GAIA])
    
    def test_user_groups_is_not_list(self):
        with pytest.raises(EntityError):
            User(name='GODOY', email="teste123@maua.br", role=ROLE.INTELICITY, groups=123)
    
    def test_user_parse_object(self):
        user = User.parse_object({
            'name': 'GODOY',
            'email': 'teste123@maua.br',
            'role': 'INTELICITY',
            'groups': ['GAIA']
        })
        assert user.name == 'Godoy'
        assert user.email == 'teste123@maua.br'
        assert user.role == ROLE.INTELICITY
        assert user.groups == [GROUPS.GAIA]

    def test_user_to_dict(self):
        user = User(name="GODOY", email="teste123@maua.br", role=ROLE.INTELICITY, groups=[GROUPS.GAIA])
        assert user.to_dict() == {
            'name': 'GODOY',
            'email': 'teste123@maua.br',
            'role': 'INTELICITY',
            'groups': ['GAIA']
        }