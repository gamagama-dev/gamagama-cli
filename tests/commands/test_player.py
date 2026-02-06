import argparse
import json

from gamagama.characters import Character, CharacterStore
from gamagama.commands.player import (
    PlayerLoadCommand,
    PlayerDropCommand,
    PlayerListCommand,
    PlayerShowCommand,
)
from gamagama.core.session import Session
from gamagama.core.tree import Tree


def _create_args(tmp_path=None):
    """Helper to create args with a valid session."""
    args = argparse.Namespace()
    tree = Tree()
    session = Session(tree)
    if tmp_path is not None:
        session.store = CharacterStore(base_dir=tmp_path)
    setattr(args, "_session", session)
    return args


def _create_char_file(tmp_path, name, data):
    """Helper to create a character JSON file."""
    char_file = tmp_path / f"{name}.json"
    char_file.write_text(json.dumps(data))
    return char_file


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

        cmd = PlayerLoadCommand()
        args = _create_args(tmp_path)
        args.name = "gandalf"

        cmd.handle(args)

        captured = capsys.readouterr()
        assert "Loaded character: Gandalf" in captured.out
        assert "gandalf" in args._session.players
        assert args._session.players["gandalf"].name == "Gandalf"

    def test_load_not_found(self, tmp_path, capsys):
        cmd = PlayerLoadCommand()
        args = _create_args(tmp_path)
        args.name = "nonexistent"

        cmd.handle(args)

        captured = capsys.readouterr()
        assert "Character file not found" in captured.out
        assert "nonexistent" not in args._session.players

    def test_load_already_loaded(self, tmp_path, capsys):
        char_data = {"name": "Gandalf"}
        _create_char_file(tmp_path, "gandalf", char_data)

        cmd = PlayerLoadCommand()
        args = _create_args(tmp_path)
        args.name = "gandalf"

        # Pre-load the character
        args._session.players["gandalf"] = Character(name="Gandalf")

        cmd.handle(args)

        captured = capsys.readouterr()
        assert "already loaded" in captured.out


class TestPlayerDrop:
    def test_drop_success(self, capsys):
        cmd = PlayerDropCommand()
        args = _create_args()
        args.name = "gandalf"

        # Pre-load the character
        args._session.players["gandalf"] = Character(name="Gandalf")

        cmd.handle(args)

        captured = capsys.readouterr()
        assert "Dropped character: gandalf" in captured.out
        assert "gandalf" not in args._session.players

    def test_drop_not_loaded(self, capsys):
        cmd = PlayerDropCommand()
        args = _create_args()
        args.name = "gandalf"

        cmd.handle(args)

        captured = capsys.readouterr()
        assert "not loaded" in captured.out


class TestPlayerList:
    def test_list_empty(self, capsys):
        cmd = PlayerListCommand()
        args = _create_args()

        cmd.handle(args)

        captured = capsys.readouterr()
        assert "No characters loaded" in captured.out

    def test_list_with_characters(self, capsys):
        cmd = PlayerListCommand()
        args = _create_args()
        args._session.players["gandalf"] = Character(name="Gandalf")
        args._session.players["frodo"] = Character(name="Frodo")

        cmd.handle(args)

        captured = capsys.readouterr()
        assert "Loaded characters:" in captured.out
        assert "gandalf" in captured.out
        assert "frodo" in captured.out


class TestPlayerShow:
    def test_show_not_loaded(self, capsys):
        cmd = PlayerShowCommand()
        args = _create_args()
        args.name = "gandalf"

        cmd.handle(args)

        captured = capsys.readouterr()
        assert "not loaded" in captured.out

    def test_show_full_character(self, capsys):
        cmd = PlayerShowCommand()
        args = _create_args()
        args.name = "gandalf"

        char = Character(
            name="Gandalf",
            system="rolemaster",
            strings={"player": "Dave", "race": "Istari"},
            stats={"strength": 75, "agility": 60},
            skills={"channeling": 85},
            counts={"hit_points": (25, 45)},
        )
        args._session.players["gandalf"] = char

        cmd.handle(args)

        captured = capsys.readouterr()
        assert "Name: Gandalf" in captured.out
        assert "System: rolemaster" in captured.out
        assert "player: Dave" in captured.out
        assert "race: Istari" in captured.out
        assert "strength: 75" in captured.out
        assert "agility: 60" in captured.out
        assert "channeling: 85" in captured.out
        assert "hit_points: 25/45" in captured.out

    def test_show_minimal_character(self, capsys):
        cmd = PlayerShowCommand()
        args = _create_args()
        args.name = "simple"

        char = Character(name="Simple")
        args._session.players["simple"] = char

        cmd.handle(args)

        captured = capsys.readouterr()
        assert "Name: Simple" in captured.out
        assert "System: generic" in captured.out
        # Should not show empty sections
        assert "Strings:" not in captured.out
        assert "Stats:" not in captured.out
        assert "Skills:" not in captured.out
        assert "Counts:" not in captured.out
