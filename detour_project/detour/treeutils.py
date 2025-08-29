"""This module provides functions for manipulating nodes in a
tree structure."""


def add_info(root, roads, parent=None):
    """Given the root of a Tree where each node
    is associated with a Road object, this method adds additional information
    to tree nodes based on associated Road objects."""
    root.parent = parent
    if root.count == 1: # if node is a leaf
        if roads[root.id].is_failing:
            root.fail_count = 1
        else:
            root.fail_count = 0

        if roads[root.id].is_selectable:
            root.selectable_count = 1
        else:
            root.selectable_count = 0
    else:
        add_info(root.left, roads, root)
        add_info(root.right, roads, root)
        root.fail_count = root.left.fail_count + root.right.fail_count
        root.selectable_count = root.left.selectable_count + root.right.selectable_count


def decrease_selectable_count(node):
    """This method decreases selectable_count values of a node and its ancestors."""
    node.selectable_count -= 1
    if node.parent is not None:
        decrease_selectable_count(node.parent)


def get_leafs_of_tree(root):
    """This method returns the leafs of a tree with the given root node."""
    if root.count == 1: # if node is a leaf
        return [root]
    else:
        return get_leafs_of_tree(root.left) + get_leafs_of_tree(root.right)
