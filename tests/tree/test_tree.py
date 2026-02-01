import pytest
from gamagama.core.tree import Tree, MapBranch, SeqBranch, Leaf, Branch


def test_tree_insert_flat():
    """Test inserting a node at the root level."""
    tree = Tree()
    leaf = tree.insert(["roll"], "roll_data")

    assert isinstance(leaf, Leaf)
    assert leaf.name == "roll"
    assert leaf.data == "roll_data"

    # Verify retrieval
    retrieved = tree.get(["roll"])
    assert retrieved == leaf


def test_tree_insert_deep():
    """Test inserting a node deeply nested."""
    tree = Tree()
    leaf = tree.insert(["player", "inventory", "add"], "add_item")

    # Verify the leaf
    assert leaf.data == "add_item"

    # Verify the structure
    root = tree.root
    assert "player" in root.children
    player_node = root.children["player"]
    assert isinstance(player_node, MapBranch)

    assert "inventory" in player_node.children
    inv_node = player_node.children["inventory"]
    assert isinstance(inv_node, MapBranch)

    assert "add" in inv_node.children
    assert inv_node.children["add"] == leaf


def test_tree_branching():
    """Test multiple leaves sharing a parent branch."""
    tree = Tree()
    tree.insert(["player", "create"], "create_fn")
    tree.insert(["player", "list"], "list_fn")
    tree.insert(["player", "delete"], "delete_fn")

    player_node = tree.get(["player"])
    assert isinstance(player_node, MapBranch)
    assert len(player_node.children) == 3
    assert set(player_node.children.keys()) == {"create", "list", "delete"}


def test_tree_get_missing():
    """Test retrieving non-existent nodes."""
    tree = Tree()
    tree.insert(["a", "b"], "data")

    assert tree.get(["a", "c"]) is None
    assert tree.get(["x"]) is None
    assert tree.get(["a", "b", "c"]) is None  # 'b' is a leaf, cannot have children


def test_illegal_traversal_through_leaf():
    """
    Test the illegal shape: trying to add a child to a node that is already a Leaf.
    Example: 'roll' is a command (Leaf), so we cannot create 'roll fast' (child).
    """
    tree = Tree()
    # 1. Create 'roll' as a Leaf
    tree.insert(["roll"], "roll_fn")

    # 2. Try to create 'roll -> fast'
    # This requires traversing 'roll', but 'roll' is a Leaf, not a Branch.
    with pytest.raises(ValueError, match="Cannot traverse 'roll': it is a Leaf"):
        tree.insert(["roll", "fast"], "fast_fn")


def test_prevent_overwrite_leaf():
    """Test that overwriting an existing Leaf raises an error."""
    tree = Tree()
    tree.insert(["roll"], "original")

    with pytest.raises(ValueError, match="Node 'roll' already exists"):
        tree.insert(["roll"], "new")


def test_prevent_overwrite_branch():
    """Test that overwriting an existing Branch with a Leaf raises an error."""
    tree = Tree()
    # Creates 'player' as a Branch
    tree.insert(["player", "create"], "create_fn")

    # Try to overwrite 'player' with a Leaf
    with pytest.raises(ValueError, match="Node 'player' already exists"):
        tree.insert(["player"], "player_fn")


def test_prevent_node_reuse_join():
    """Test that a node cannot be added to multiple branches (no joins)."""
    tree = Tree()
    leaf = tree.insert(["a"], "data")

    # Manually create a second branch attached to root
    branch_b = MapBranch(name="b")
    tree.root.add_child(branch_b)

    # Try to add the existing leaf to branch_b
    with pytest.raises(ValueError, match="already has a parent"):
        branch_b.add_child(leaf)


def test_seq_branch():
    """Test SeqBranch behavior (ordered children, duplicates allowed)."""
    seq = SeqBranch(name="sequence")
    
    leaf1 = Leaf(name="item", data=1)
    leaf2 = Leaf(name="item", data=2)
    
    seq.add_child(leaf1)
    seq.add_child(leaf2)
    
    assert len(seq.children) == 2
    assert seq.children[0] == leaf1
    assert seq.children[1] == leaf2
    
    # Iteration check
    items = list(seq)
    assert items == [leaf1, leaf2]


def test_walk():
    """Test the walk method traverses the tree correctly."""
    tree = Tree()
    # Structure:
    # root
    #  |- a (Leaf)
    #  |- b (MapBranch)
    #      |- c (Leaf)
    
    tree.insert(["a"], "data_a")
    tree.insert(["b", "c"], "data_c")
    
    nodes = list(tree.walk())
    names = [n.name for n in nodes]
    
    # Order: root -> a -> b -> c (assuming insertion order is preserved)
    assert names == ["root", "a", "b", "c"]


def test_walk_polymorphic():
    """Test walking a tree containing both MapBranch and SeqBranch."""
    # root (Map)
    #  |- expr (Seq)
    #      |- 1 (Leaf)
    #      |- + (Leaf)
    #      |- 2 (Leaf)
    
    root = MapBranch(name="root")
    expr = SeqBranch(name="expr")
    root.add_child(expr)
    
    l1 = Leaf(name="1")
    op = Leaf(name="+")
    l2 = Leaf(name="2")
    
    expr.add_child(l1)
    expr.add_child(op)
    expr.add_child(l2)
    
    # Manually construct tree wrapper to use walk
    tree = Tree()
    tree.root = root
    
    nodes = list(tree.walk())
    names = [n.name for n in nodes]
    
    assert names == ["root", "expr", "1", "+", "2"]


def test_insert_traversal_fails_on_seq_branch():
    """Test that Tree.insert cannot traverse through a SeqBranch."""
    tree = Tree()

    # Manually inject a SeqBranch
    seq = SeqBranch(name="sequence")
    tree.root.add_child(seq)

    # Try to insert a child *under* the sequence using path notation
    # This implies "sequence" maps to a child named "item", which SeqBranch doesn't support.
    with pytest.raises(ValueError, match="current node is not a MapBranch"):
        tree.insert(["sequence", "item"], "data")
