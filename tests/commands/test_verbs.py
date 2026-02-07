"""Tests for global verb commands."""
import argparse
import json

from gamagama.cli.characters import Character, CharacterStore
from gamagama.cli.commands.verbs import (
    ShowCommand,
    ListCommand,
    SetCommand,
    LoadCommand,
    DropCommand,
)
from gamagama.cli.commands.player import PlayerDomain
from gamagama.cli.commands.system import SystemDomain
from gamagama.cli.core.session import Session
from gamagama.cli.core.registry import CommandTree
from gamagama.cli.commands import discover_commands


def _create_session(tmp_path=None):
    """Helper to create a session with discovered commands."""
    tree = CommandTree()
    discover_commands(tree)
    session = Session(tree)
    if tmp_path is not None:
        session.store = CharacterStore(base_dir=tmp_path)
    return session


def _create_args(session, **kwargs):
    """Helper to create args namespace."""
    args = argparse.Namespace()
    args._session = session
    args._interactive = True
    for key, value in kwargs.items():
        setattr(args, key, value)
    return args


class TestShowCommand:
    def test_show_at_root(self, capsys):
        session = _create_session()
        cmd = ShowCommand()
        args = _create_args(session, target=None, name=None)

        cmd.handle(args)

        captured = capsys.readouterr()
        assert "system: generic" in captured.out
        assert "player: (none)" in captured.out

    def test_show_specific_domain(self, capsys):
        session = _create_session()
        cmd = ShowCommand()
        args = _create_args(session, target="system", name=None)

        cmd.handle(args)

        captured = capsys.readouterr()
        # System has nested domains, so should show nested actives
        # Schema domain shows "(none)" when no schema is set
        assert "schema: (none)" in captured.out

    def test_show_in_player_context(self, capsys):
        session = _create_session()
        session.players["gandalf"] = Character(name="Gandalf")
        session.active_player = "gandalf"

        # Navigate to player domain
        player_domain = session.tree.root.get_child("player")
        session.current_node = player_domain

        cmd = ShowCommand()
        args = _create_args(session, target=None, name=None)

        cmd.handle(args)

        captured = capsys.readouterr()
        assert "Name: Gandalf" in captured.out


class TestListCommand:
    def test_list_system(self, capsys):
        session = _create_session()
        cmd = ListCommand()
        args = _create_args(session, domain="system")

        cmd.handle(args)

        captured = capsys.readouterr()
        assert "generic" in captured.out
        assert "rolemaster" in captured.out

    def test_list_player_empty(self, capsys):
        session = _create_session()
        cmd = ListCommand()
        args = _create_args(session, domain="player")

        cmd.handle(args)

        captured = capsys.readouterr()
        assert "No players available" in captured.out

    def test_list_player_with_active(self, capsys):
        session = _create_session()
        session.players["gandalf"] = Character(name="Gandalf")
        session.players["frodo"] = Character(name="Frodo")
        session.active_player = "gandalf"

        cmd = ListCommand()
        args = _create_args(session, domain="player")

        cmd.handle(args)

        captured = capsys.readouterr()
        assert "* gandalf" in captured.out
        assert "  frodo" in captured.out

    def test_list_in_context(self, capsys):
        session = _create_session()

        # Navigate to system domain
        system_domain = session.tree.root.get_child("system")
        session.current_node = system_domain

        cmd = ListCommand()
        args = _create_args(session, domain=None)

        cmd.handle(args)

        captured = capsys.readouterr()
        assert "generic" in captured.out
        assert "rolemaster" in captured.out


class TestSetCommand:
    def test_set_system(self, capsys):
        session = _create_session()
        cmd = SetCommand()
        args = _create_args(session, target="system", name="rolemaster")

        cmd.handle(args)

        captured = capsys.readouterr()
        assert "System changed to: rolemaster" in captured.out
        assert session.system.name == "rolemaster"

    def test_set_player_not_loaded(self, capsys):
        session = _create_session()
        cmd = SetCommand()
        args = _create_args(session, target="player", name="gandalf")

        cmd.handle(args)

        captured = capsys.readouterr()
        assert "not found" in captured.out.lower()

    def test_set_in_context(self, capsys):
        session = _create_session()
        session.players["gandalf"] = Character(name="Gandalf")

        # Navigate to player domain
        player_domain = session.tree.root.get_child("player")
        session.current_node = player_domain

        cmd = SetCommand()
        args = _create_args(session, target="gandalf", name=None)

        cmd.handle(args)

        # Should work without output (silent success)
        assert session.active_player == "gandalf"


class TestLoadCommand:
    def test_load_player(self, tmp_path, capsys):
        char_data = {"name": "Gandalf", "system": "generic"}
        char_file = tmp_path / "gandalf.json"
        char_file.write_text(json.dumps(char_data))

        session = _create_session(tmp_path)
        cmd = LoadCommand()
        args = _create_args(session, target="player", name="gandalf")

        cmd.handle(args)

        captured = capsys.readouterr()
        assert "Loaded character: Gandalf" in captured.out
        assert "gandalf" in session.players

    def test_load_unsupported_verb(self, capsys):
        session = _create_session()
        cmd = LoadCommand()
        args = _create_args(session, target="system", name="generic")

        cmd.handle(args)

        captured = capsys.readouterr()
        assert "not available" in captured.out.lower()


class TestDropCommand:
    def test_drop_player(self, capsys):
        session = _create_session()
        session.players["gandalf"] = Character(name="Gandalf")

        cmd = DropCommand()
        args = _create_args(session, target="player", name="gandalf")

        cmd.handle(args)

        captured = capsys.readouterr()
        assert "Dropped character: gandalf" in captured.out
        assert "gandalf" not in session.players

    def test_drop_active_player(self, capsys):
        session = _create_session()
        session.players["gandalf"] = Character(name="Gandalf")
        session.active_player = "gandalf"

        # Navigate to player domain
        player_domain = session.tree.root.get_child("player")
        session.current_node = player_domain

        cmd = DropCommand()
        args = _create_args(session, target=None, name=None)

        cmd.handle(args)

        captured = capsys.readouterr()
        assert "Dropped character: gandalf" in captured.out
        assert session.active_player is None

    def test_drop_unsupported_verb(self, capsys):
        session = _create_session()
        cmd = DropCommand()
        args = _create_args(session, target="system", name="generic")

        cmd.handle(args)

        captured = capsys.readouterr()
        assert "not available" in captured.out.lower()
