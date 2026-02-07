"""Tests for the SchemaDomain."""
from gamagama.commands.system.schema import SchemaDomain
from gamagama.core.session import Session
from gamagama.core.tree import Tree
from gamagama.systems import RolemasterSystem, GenericSystem


def _create_session(system_class=GenericSystem):
    """Helper to create a session."""
    tree = Tree()
    return Session(tree, system=system_class())


class TestSchemaDomain:
    def test_list_items_empty(self):
        session = _create_session(GenericSystem)
        domain = SchemaDomain()

        # Generic system has no schemas
        items = domain.list_items(session)
        assert items == []

    def test_get_active_none(self):
        session = _create_session()
        domain = SchemaDomain()

        assert domain.get_active(session) is None

    def test_get_active_set(self):
        session = _create_session()
        session.active_schema = "test"
        domain = SchemaDomain()

        assert domain.get_active(session) == "test"

    def test_set_active_not_found(self, capsys):
        session = _create_session()
        domain = SchemaDomain()

        result = domain.set_active(session, "nonexistent")

        assert result is False
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower()

    def test_show_item_no_active(self):
        session = _create_session()
        domain = SchemaDomain()

        result = domain.show_item(session, None)
        assert result is None

    def test_has_nested_domains(self):
        session = _create_session()
        domain = SchemaDomain()

        assert domain.has_nested_domains() is False

    def test_get_nested_actives(self):
        session = _create_session()
        domain = SchemaDomain()

        assert domain.get_nested_actives(session) == {}
