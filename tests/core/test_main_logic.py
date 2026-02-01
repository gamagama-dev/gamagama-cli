from gamagama.core.main import _resolve_node, _build_prompt_path
from gamagama.core.tree import MapBranch, Tree

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
    # root -> branch -> sub
    branch = MapBranch(name="branch")
    tree.root.add_child(branch)
    sub = MapBranch(name="sub")
    branch.add_child(sub)
    
    assert _build_prompt_path(tree.root) == ""
    assert _build_prompt_path(branch) == "/branch"
    assert _build_prompt_path(sub) == "/branch/sub"
