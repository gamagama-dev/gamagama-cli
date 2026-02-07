from gamagama.cli.core.main import _resolve_node, _build_prompt_path
from gamagama.cli.core.tree import MapBranch, Tree
from gamagama.cli.core.session import Session
from gamagama.cli.core.domain import DomainBranch


def test_resolve_node_local():
    tree = Tree()
    child = tree.insert(["local"], "data")

    # Should find 'local' in root
    found = _resolve_node(tree.root, "local")
    assert found == child


def test_resolve_node_bubbling():
    tree = Tree()
    root_cmd = tree.insert(["global"], "data")

    # Create a child branch
    branch = MapBranch(name="branch")
    tree.root.add_child(branch)

    # Search for 'global' starting from 'branch'
    found = _resolve_node(branch, "global")
    assert found == root_cmd


def test_resolve_node_not_found():
    tree = Tree()
    branch = MapBranch(name="branch")
    tree.root.add_child(branch)

    found = _resolve_node(branch, "nonexistent")
    assert found is None


def test_build_prompt_path():
    tree = Tree()
    session = Session(tree)

    # root -> branch -> sub
    branch = MapBranch(name="branch")
    tree.root.add_child(branch)
    sub = MapBranch(name="sub")
    branch.add_child(sub)

    assert _build_prompt_path(tree.root, session) == ""
    assert _build_prompt_path(branch, session) == "branch"
    assert _build_prompt_path(sub, session) == "branch sub"


def test_build_prompt_path_with_domain():
    tree = Tree()
    session = Session(tree)
    session.active_player = "active_item"

    # Use PlayerDomain which is a real domain
    from gamagama.cli.commands.player import PlayerDomain
    domain = PlayerDomain()
    tree.root.add_child(domain)

    # First add a player so get_active can return it
    from gamagama.cli.characters import Character
    session.players["active_item"] = Character(name="Active Item")

    assert _build_prompt_path(domain, session) == "player (active_item)"


def test_build_prompt_path_domain_no_active():
    tree = Tree()
    session = Session(tree)

    # Use PlayerDomain which is a real domain
    from gamagama.cli.commands.player import PlayerDomain
    domain = PlayerDomain()
    tree.root.add_child(domain)

    assert _build_prompt_path(domain, session) == "player"
