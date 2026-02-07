import pytest
from dataclasses import dataclass
from gamagama.cli.core.tree import Tree, SeqBranch, Leaf, NodeVisitor


def test_visitor_pattern():
    """Test that the visitor pattern correctly dispatches to node types."""
    
    class TestVisitor(NodeVisitor):
        def __init__(self):
            self.visited = []

        def visit_MapBranch(self, node):
            self.visited.append(f"map:{node.name}")
            # Manually traverse children for this test
            for child in node:
                self.visit(child)

        def visit_SeqBranch(self, node):
            self.visited.append(f"seq:{node.name}")
            for child in node:
                self.visit(child)

        def visit_Leaf(self, node):
            self.visited.append(f"leaf:{node.name}")

    # Build a tree: root(Map) -> seq(Seq) -> item(Leaf)
    tree = Tree()
    seq = SeqBranch(name="seq")
    tree.root.add_child(seq)
    leaf = Leaf(name="item")
    seq.add_child(leaf)
    
    visitor = TestVisitor()
    visitor.visit(tree.root)
    
    assert visitor.visited == ["map:root", "seq:seq", "leaf:item"]


def test_visitor_mro_dispatch():
    """Test that the visitor walks the MRO to find a handler."""
    
    @dataclass(eq=False)
    class SpecialLeaf(Leaf):
        pass

    class MroVisitor(NodeVisitor):
        def __init__(self):
            self.log = []

        def visit_Leaf(self, node):
            self.log.append(f"leaf:{node.name}")

        def visit_SpecialLeaf(self, node):
            self.log.append(f"special:{node.name}")

    class FallbackVisitor(NodeVisitor):
        def __init__(self):
            self.log = []

        def visit_Leaf(self, node):
            self.log.append(f"leaf_fallback:{node.name}")

    leaf = Leaf(name="normal")
    special = SpecialLeaf(name="special")

    # Case 1: Specific handler exists
    v1 = MroVisitor()
    v1.visit(leaf)
    v1.visit(special)
    assert v1.log == ["leaf:normal", "special:special"]

    # Case 2: Fallback to parent handler
    v2 = FallbackVisitor()
    v2.visit(leaf)
    v2.visit(special)
    assert v2.log == ["leaf_fallback:normal", "leaf_fallback:special"]


def test_visitor_generic_fallback():
    """Test that visitor falls back to generic_visit if no handler found."""
    
    class GenericVisitor(NodeVisitor):
        def __init__(self):
            self.visited = []
            
        def generic_visit(self, node):
            self.visited.append(f"generic:{node.name}")

    leaf = Leaf(name="item")
    visitor = GenericVisitor()
    visitor.visit(leaf)
    
    assert visitor.visited == ["generic:item"]
