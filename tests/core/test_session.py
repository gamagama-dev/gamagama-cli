from gamagama.cli.characters import CharacterStore
from gamagama.cli.core.session import Session
from gamagama.cli.core.tree import Tree


def test_session_init():
    tree = Tree()
    session = Session(tree)

    assert session.tree == tree
    assert session.current_node == tree.root
    assert session.should_exit is False
    assert isinstance(session.store, CharacterStore)
    assert session.players == {}
