import argparse
import json

from gamagama.cli.characters import Character, CharacterStore
from gamagama.cli.commands.player import PlayerDomain
from gamagama.cli.core.session import Session
from gamagama.cli.core.tree import Tree


def _create_session(tmp_path=None):
    """Helper to create a session for testing."""
    tree = Tree()
    session = Session(tree)
    if tmp_path is not None:
        session.store = CharacterStore(base_dir=tmp_path)
    return session


def _create_char_file(tmp_path, name, data):
    """Helper to create a character JSON file."""
    char_file = tmp_path / f"{name}.json"
    char_file.write_text(json.dumps(data))
    return char_file


class TestPlayerDomain:
    def test_list_items_empty(self):
        session = _create_session()
        domain = PlayerDomain()

        items = domain.list_items(session)
        assert items == []

    def test_list_items_with_players(self):
        session = _create_session()
        session.players["gandalf"] = Character(name="Gandalf")
        session.players["frodo"] = Character(name="Frodo")
        domain = PlayerDomain()

        items = domain.list_items(session)
        assert "gandalf" in items
        assert "frodo" in items

    def test_get_active_none(self):
        session = _create_session()
        domain = PlayerDomain()

        assert domain.get_active(session) is None

    def test_set_active_success(self):
        session = _create_session()
        session.players["gandalf"] = Character(name="Gandalf")
        domain = PlayerDomain()

        result = domain.set_active(session, "gandalf")
        assert result is True
        assert session.active_player == "gandalf"

    def test_set_active_not_found(self):
        session = _create_session()
        domain = PlayerDomain()

        result = domain.set_active(session, "nonexistent")
        assert result is False
        assert session.active_player is None


class TestPlayerLoad:
    def test_load_success(self, tmp_path, capsys):
        char_data = {
            "name": "Gandalf",
            "system": "rolemaster",
            "strings": {"player": "Dave"},
            "stats": {"strength": 75},
            "skills": {"channeling": 85},
            "counts": {"hit_points": [25, 45]},
        }
        _create_char_file(tmp_path, "gandalf", char_data)

        session = _create_session(tmp_path)
        domain = PlayerDomain()

        result = domain.load_item(session, "gandalf")

        assert result is True
        captured = capsys.readouterr()
        assert "Loaded character: Gandalf" in captured.out
        assert "gandalf" in session.players
        assert session.players["gandalf"].name == "Gandalf"

    def test_load_not_found(self, tmp_path, capsys):
        session = _create_session(tmp_path)
        domain = PlayerDomain()

        result = domain.load_item(session, "nonexistent")

        assert result is False
        captured = capsys.readouterr()
        assert "Character file not found" in captured.out
        assert "nonexistent" not in session.players

    def test_load_already_loaded(self, tmp_path, capsys):
        char_data = {"name": "Gandalf"}
        _create_char_file(tmp_path, "gandalf", char_data)

        session = _create_session(tmp_path)
        session.players["gandalf"] = Character(name="Gandalf")
        domain = PlayerDomain()

        result = domain.load_item(session, "gandalf")

        assert result is False
        captured = capsys.readouterr()
        assert "already loaded" in captured.out


class TestPlayerDrop:
    def test_drop_success(self, capsys):
        session = _create_session()
        session.players["gandalf"] = Character(name="Gandalf")
        domain = PlayerDomain()

        result = domain.drop_item(session, "gandalf")

        assert result is True
        captured = capsys.readouterr()
        assert "Dropped character: gandalf" in captured.out
        assert "gandalf" not in session.players

    def test_drop_not_loaded(self, capsys):
        session = _create_session()
        domain = PlayerDomain()

        result = domain.drop_item(session, "gandalf")

        assert result is False
        captured = capsys.readouterr()
        assert "not loaded" in captured.out

    def test_drop_active_player(self, capsys):
        session = _create_session()
        session.players["gandalf"] = Character(name="Gandalf")
        session.active_player = "gandalf"
        domain = PlayerDomain()

        result = domain.drop_item(session, "gandalf")

        assert result is True
        assert session.active_player is None
        captured = capsys.readouterr()
        assert "Active player cleared" in captured.out

    def test_drop_defaults_to_active(self, capsys):
        session = _create_session()
        session.players["gandalf"] = Character(name="Gandalf")
        session.active_player = "gandalf"
        domain = PlayerDomain()

        result = domain.drop_item(session, None)

        assert result is True
        assert "gandalf" not in session.players


class TestPlayerShow:
    def test_show_not_loaded(self):
        session = _create_session()
        domain = PlayerDomain()

        result = domain.show_item(session, "gandalf")
        assert result is None

    def test_show_full_character(self):
        session = _create_session()
        char = Character(
            name="Gandalf",
            system="rolemaster",
            strings={"player": "Dave", "race": "Istari"},
            stats={"strength": 75, "agility": 60},
            skills={"channeling": 85},
            counts={"hit_points": (25, 45)},
        )
        session.players["gandalf"] = char
        domain = PlayerDomain()

        result = domain.show_item(session, "gandalf")

        assert "Name: Gandalf" in result
        assert "System: rolemaster" in result
        assert "player: Dave" in result
        assert "race: Istari" in result
        assert "strength: 75" in result
        assert "agility: 60" in result
        assert "channeling: 85" in result
        assert "hit_points: 25/45" in result

    def test_show_minimal_character(self):
        session = _create_session()
        char = Character(name="Simple")
        session.players["simple"] = char
        domain = PlayerDomain()

        result = domain.show_item(session, "simple")

        assert "Name: Simple" in result
        assert "System: generic" in result
        # Should not show empty sections
        assert "Strings:" not in result
        assert "Stats:" not in result
        assert "Skills:" not in result
        assert "Counts:" not in result

    def test_show_defaults_to_active(self):
        session = _create_session()
        session.players["gandalf"] = Character(name="Gandalf")
        session.active_player = "gandalf"
        domain = PlayerDomain()

        result = domain.show_item(session, None)

        assert "Name: Gandalf" in result
