"""Tests for the domain infrastructure."""
from dataclasses import dataclass, field
from typing import Set

from gamagama.core.domain import Domain, DomainBranch
from gamagama.core.tree import Tree
from gamagama.core.session import Session


def test_domain_branch_is_domain():
    """DomainBranch should satisfy the Domain protocol."""
    domain = DomainBranch(name="test")
    assert isinstance(domain, Domain)


def test_domain_branch_defaults():
    """DomainBranch should have sensible defaults."""
    tree = Tree()
    session = Session(tree)
    domain = DomainBranch(name="test")

    assert domain.list_items(session) == []
    assert domain.get_active(session) is None
    assert domain.set_active(session, "foo") is False
    assert domain.show_item(session, None) is None
    assert domain.has_nested_domains() is False
    assert domain.get_nested_actives(session) == {}
    assert domain.load_item(session, "foo") is False
    assert domain.drop_item(session, None) is False


def test_domain_branch_supported_verbs():
    """DomainBranch should track supported verbs."""
    domain = DomainBranch(name="test", supported_verbs={"show", "list"})
    assert domain.supported_verbs == {"show", "list"}


def test_domain_branch_as_map_branch():
    """DomainBranch should work as a MapBranch for tree operations."""
    tree = Tree()
    parent = DomainBranch(name="parent")
    tree.root.add_child(parent)

    child = DomainBranch(name="child")
    parent.add_child(child)

    assert parent.get_child("child") == child
    assert child.parent == parent
