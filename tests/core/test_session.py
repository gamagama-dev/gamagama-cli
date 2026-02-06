from gamagama.characters import CharacterStore
from gamagama.core.session import Session
from gamagama.core.tree import Tree


def test_session_init():
    tree = Tree()
    session = Session(tree)

    assert session.tree == tree
    assert session.current_node == tree.root
    assert session.should_exit is False
    assert isinstance(session.store, CharacterStore)
    assert session.players == {}
