from unittest.mock import patch
from gamagama.core.completer import Completer
from gamagama.core.tree import Tree, MapBranch
from gamagama.core.session import Session

def test_complete_local():
    tree = Tree()
    tree.insert(["add"], "cmd")
    
    session = Session(tree)
    completer = Completer(tree, session)
    
    with patch("gamagama.core.completer.readline") as mock_rl:
        mock_rl.get_line_buffer.return_value = "ad"
        
        res = completer.complete("ad", 0)
        assert res == "add"

def test_complete_bubbling():
    tree = Tree()
    tree.insert(["roll"], "cmd") # root command
    
    branch = MapBranch(name="player")
    tree.root.add_child(branch)
    
    session = Session(tree)
    session.current_node = branch
    
    completer = Completer(tree, session)
    
    with patch("gamagama.core.completer.readline") as mock_rl:
        # Case: User types "ro" inside player
        mock_rl.get_line_buffer.return_value = "ro"
        
        # state 0 should return "roll"
        res = completer.complete("ro", 0)
        assert res == "roll"

def test_complete_path():
    tree = Tree()
    tree.insert(["player", "add"], "cmd")
    
    session = Session(tree)
    # At root
    completer = Completer(tree, session)
    
    with patch("gamagama.core.completer.readline") as mock_rl:
        # Case: User types "player a"
        mock_rl.get_line_buffer.return_value = "player a"
        
        res = completer.complete("a", 0)
        assert res == "add"
