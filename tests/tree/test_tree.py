import pytest
from gamagama.core.tree import Tree, Branch, Leaf


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
    assert isinstance(player_node, Branch)

    assert "inventory" in player_node.children
    inv_node = player_node.children["inventory"]
    assert isinstance(inv_node, Branch)

    assert "add" in inv_node.children
    assert inv_node.children["add"] == leaf


def test_tree_branching():
    """Test multiple leaves sharing a parent branch."""
    tree = Tree()
    tree.insert(["player", "create"], "create_fn")
    tree.insert(["player", "list"], "list_fn")
    tree.insert(["player", "delete"], "delete_fn")

    player_node = tree.get(["player"])
    assert isinstance(player_node, Branch)
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


def test_overwrite_branch_with_leaf():
    """
    Test overwriting a Branch with a Leaf.
    This is technically allowed by the data structure (it orphans the children),
    though usually undesirable in logic. We test it to ensure deterministic behavior.
    """
    tree = Tree()
    # 1. Create 'player -> create' (player is a Branch)
    tree.insert(["player", "create"], "create_fn")
    assert isinstance(tree.get(["player"]), Branch)

    # 2. Overwrite 'player' with a Leaf
    tree.insert(["player"], "player_fn")

    node = tree.get(["player"])
    assert isinstance(node, Leaf)
    assert node.data == "player_fn"

    # The children are effectively lost/orphaned from the tree
    # (The Branch object might still exist in memory if referenced, but is detached from root)
