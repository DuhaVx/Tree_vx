from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Tuple


@dataclass
class TreeNode:
    """A node in the binary search tree."""

    key: Any
    value: Any
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None

    def __repr__(self) -> str:
        return f"TreeNode(key={self.key!r}, value={self.value!r})"


class BinarySearchTree:
    """Binary Search Tree that stores key-value pairs."""

    def __init__(self) -> None:
        self.root: Optional[TreeNode] = None

    # Public API
    def insert(self, key: Any, value: Any) -> None:
        """Insert a key-value pair into the tree. Updates value if key exists."""
        if self.root is None:
            self.root = TreeNode(key, value)
            return

        current = self.root
        while current:
            if key == current.key:
                current.value = value
                return
            if key < current.key:
                if current.left is None:
                    current.left = TreeNode(key, value)
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = TreeNode(key, value)
                    return
                current = current.right

    def search(self, key: Any) -> Optional[Any]:
        """Return the value associated with key, or None if not found."""
        current = self.root
        while current:
            if key == current.key:
                return current.value
            current = current.left if key < current.key else current.right
        return None

    def delete(self, key: Any) -> bool:
        """Delete the node with the given key. Returns True if removed."""

        def _delete(node: Optional[TreeNode], target: Any) -> Tuple[Optional[TreeNode], bool]:
            if node is None:
                return None, False

            if target < node.key:
                node.left, removed = _delete(node.left, target)
                return node, removed
            if target > node.key:
                node.right, removed = _delete(node.right, target)
                return node, removed

            # Node found: handle three structural cases
            if node.left is None and node.right is None:
                return None, True
            if node.left is None:
                return node.right, True
            if node.right is None:
                return node.left, True

            # Replace with in-order successor (smallest in right subtree)
            successor = node.right
            while successor.left:
                successor = successor.left
            node.key, node.value = successor.key, successor.value
            node.right, _ = _delete(node.right, successor.key)
            return node, True

        self.root, removed_flag = _delete(self.root, key)
        return removed_flag

    def height(self) -> int:
        """
        Return the height of the tree.

        Height is defined as the number of nodes on the longest path
        from the root down to a leaf. Empty tree has height 0.
        """

        def _height(node: Optional[TreeNode]) -> int:
            if node is None:
                return 0
            return 1 + max(_height(node.left), _height(node.right))

        return _height(self.root)

    def is_balanced(self) -> bool:
        """
        Check whether the tree is height-balanced.

        A balanced tree is one where the height difference between
        the left and right subtrees of every node is at most 1.
        """

        def _check(node: Optional[TreeNode]) -> Tuple[int, bool]:
            if node is None:
                return 0, True

            left_height, left_balanced = _check(node.left)
            right_height, right_balanced = _check(node.right)
            height = 1 + max(left_height, right_height)
            balanced = (
                left_balanced
                and right_balanced
                and abs(left_height - right_height) <= 1
            )
            return height, balanced

        _, balanced_flag = _check(self.root)
        return balanced_flag


def _demo() -> None:
    """Simple manual demonstration of the BST API."""
    tree = BinarySearchTree()
    for key, value in [(5, "root"), (3, "left"), (7, "right"), (2, "leaf"), (4, "mid")]:
        tree.insert(key, value)

    print("Initial height:", tree.height())
    print("Is balanced:", tree.is_balanced())
    print("Search 4 ->", tree.search(4))

    print("Delete 3:", tree.delete(3))
    print("Search 3 ->", tree.search(3))
    print("Height after delete:", tree.height())
    print("Is balanced after delete:", tree.is_balanced())


if __name__ == "__main__":
    _demo()

