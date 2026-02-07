from gamagama.cli.commands.system import SystemDomain
from gamagama.cli.core.session import Session
from gamagama.cli.core.tree import Tree
from gamagama.cli.systems import RolemasterSystem, GenericSystem


def _create_session():
    """Helper to create a session for testing."""
    tree = Tree()
    return Session(tree)


class TestSystemDomain:
    def test_list_items(self):
        session = _create_session()
        domain = SystemDomain()

        items = domain.list_items(session)

        assert "generic" in items
        assert "rolemaster" in items

    def test_get_active_default(self):
        session = _create_session()
        domain = SystemDomain()

        active = domain.get_active(session)
        assert active == "generic"

    def test_set_active_valid(self, capsys):
        session = _create_session()
        domain = SystemDomain()

        result = domain.set_active(session, "rolemaster")

        assert result is True
        assert isinstance(session.system, RolemasterSystem)
        captured = capsys.readouterr()
        assert "System changed to: rolemaster" in captured.out

    def test_set_active_invalid(self, capsys):
        session = _create_session()
        domain = SystemDomain()

        result = domain.set_active(session, "invalid_game")

        assert result is False
        captured = capsys.readouterr()
        assert "System 'invalid_game' not found" in captured.out
        # Should remain Generic
        assert isinstance(session.system, GenericSystem)

    def test_set_active_clears_schema(self):
        session = _create_session()
        session.active_schema = "character"
        domain = SystemDomain()

        domain.set_active(session, "rolemaster")

        # Changing system should clear schema
        assert session.active_schema is None

    def test_show_item(self):
        session = _create_session()
        domain = SystemDomain()

        result = domain.show_item(session, None)
        assert result == "System: generic"

    def test_has_nested_domains(self):
        session = _create_session()
        domain = SystemDomain()

        assert domain.has_nested_domains() is True

    def test_get_nested_actives_none(self):
        session = _create_session()
        domain = SystemDomain()

        nested = domain.get_nested_actives(session)
        assert nested == {}

    def test_get_nested_actives_with_schema(self):
        session = _create_session()
        session.active_schema = "character"
        domain = SystemDomain()

        nested = domain.get_nested_actives(session)
        assert nested == {"schema": "character"}
