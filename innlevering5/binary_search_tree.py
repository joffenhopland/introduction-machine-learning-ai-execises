import warnings
from binarytree import Node


class BinarySearchTree:

    def __init__(self, root=None):
        """ Initialize binary search tree

        # Inputs:
        root:    (optional) An instance of Node which is the root of the tree

        # Notes:
        If a root is supplied, validate that the tree meets the requirements
        of a search tree. If not, raise ValueError.
        """
        self.root = root
        # if BinarySearchTree.is_BST_valid(root) == False:
        #     raise ValueError("The The tree is not a binary search tree")

    def is_BST_valid(self, root, min=float('-inf'), max=float('inf')):
        # recurrsion
        # it's a BST if the tree is empty
        if root is None:
            return True
        if root.value <= min or root.value >= max:
            return False
        # root is the new max in left branch, root is the new min in right branch
        return self.is_BST_valid(root.left, min, root.value) and self.is_BST_valid(root.right, root.value, max)

    def insert(self, value):
        """ Insert a new node into the tree

        # Inputs:
        value:    Value of new node

        # Notes:
        The method should issue a warning if the value already exists in the tree.
        See https://docs.python.org/3/library/warnings.html#warnings.warn
        In the case of duplicate values, leave the tree unchanged.
        """

        if self.root is None:
            self.root = Node(value)
            return self.root
        else:
            return self._insert(self.root, value)

    def _insert(self, node, value):
        # Check if value already exists
        if value == node.value:
            # Issue a warning that the value already exists here
            warnings.warn(message="value already exists in the tree!")
            # Leave tree unchanged
            return None
        # check left branch
        elif value < node.value:
            if node.left is not None:
                return self._insert(node.left, value)
            else:
                # if child is empty, then add new Node
                node.left = Node(value)
                return node.left
        else:
            # check right branch
            if node.right is None:
                node.right = Node(value)
                return node.right
            else:
                return self._insert(node.right, value)

    def find(self, value):
        """ Find node with given value, return node

        # Inputs:
        value:    Value of node to be found

        # Returns:
        node:     Node object containing given value

        # Notes:
        - The function should raise a KeyError if the value
        is not found in the tree.
        """

        return self._find(self.root, value)

    def _find(self, node, value):
        if node is None:
            raise KeyError("Value not found")  # value not found
            # return None
        elif node.value == value:
            return node  # value found
        elif node.value > value:  # search left subtree
            return self._find(node.left, value)
        else:
            return self._find(node.right, value)  # search right subtree

    def delete(self, value):
        """ Delete node with given value

        # Inputs:
        value:    Value of node to be deleted

        # Notes:
        This function should handle a number of "regular" cases:
        - Deleting a leaf node
        - Deleting a node with one child
        - Deleting a node with two childen
          (the node should be replaced with its inorder successor)

        It should also handle the following "edge cases":
        - Value not found in tree (raise KeyError)
        - Deleting the root node
        - Calling delete on an empty tree (raise KeyError)
        """

        if self.root is None:
            raise KeyError("The tree is empty")

        node = self.find(value)

        if node is None:
            raise KeyError("Value not found in tree")

        return self._delete(node, value)

    def _delete(self, node, value):
        # must know the parent node of the node that is going to be deleted
        # print(f'self.root: {self.root.value}')
        # print(f'node: {node}')
        tree = BinarySearchTree()

        node_and_parent = tree.find_with_parent(self.root, value)
        # print(f'node_and_parent: {node_and_parent}')
        # print(f'node_and_parent[0]: {node_and_parent[0]}')
        # print(f'node_and_parent[1]: {node_and_parent[1]}')

        node = node_and_parent[0]
        parent = node_and_parent[1]

        if node.left is None and node.right is None:
            tree.delete_node_with_no_children(
                node, parent)
        elif (node.left is None and node.right is not None) or (node.right is None and node.left is not None):
            tree.delete_node_with_one_child(
                node, parent)
        else:
            tree.delete_node_with_two_children(
                node, parent)

    def find_with_parent(self, root, value):
        current_node = root
        parent = None
        done = False
        while not done:
            if value == current_node.value:
                done = True
            elif value < current_node.value and current_node.left:
                parent = current_node
                current_node = current_node.left
            elif value > current_node.value and current_node.right:
                parent = current_node
                current_node = current_node.right
            else:
                raise KeyError("Value not found")
        return current_node, parent

    def delete_node_with_no_children(self, node, parent):
        if parent.left == node:
            parent.left = None
        elif parent.right == node:
            parent.right = None

    def delete_node_with_one_child(self, node, parent):
        if node.right and node.left == None:  # node to remove has only right child
            if parent.right == node:
                temp = node.right
                node = None
                parent.right = temp
            if parent.left == node:
                temp = node.right
                node = None
                parent.left = temp

        elif node.left and node.right == None:  # node to remove has only left child
            if parent.right == node:
                temp = node.left
                node = None
                parent.right = temp
            if parent.left == node:
                temp = node.left
                node = None
                parent.left = temp

    def delete_node_with_two_children(self, node, parent):
        tree = BinarySearchTree()
        successor = tree.find_successor_with_parent(node, parent)
        successor_node = successor[0]
        successor_node_parent = successor[1]
        node.value = successor_node.value

        # delete successor
        if successor_node.left is None and successor_node.right is None:
            tree.delete_node_with_no_children(
                successor_node, successor_node_parent)
        elif (successor_node.left is None and successor_node.right is not None) or (successor_node.right is None and successor_node.left is not None):
            tree.delete_node_with_one_child(
                successor_node, successor_node_parent)
        else:
            tree.delete_node_with_two_children(
                successor_node, successor_node_parent)

    def find_successor_with_parent(self, node, parent):
        if node.right:
            parent = node
            node = node.right
            while node.left:
                parent = node
                node = node.left
        return node, parent

    def level(self, value):

        root = self.root
        lst = []
        level = 1
        lst.append(root)

        lst.append(None)
        while (len(lst)):
            temp = lst[0]
            lst.pop(0)
            if (temp == None):
                if len(lst) == 0:
                    return 0
                if (lst[0] != None):
                    lst.append(None)
                level += 1
            else:
                if (temp.value == value):
                    return level
                if (temp.left):
                    lst.append(temp.left)
                if (temp.right):
                    lst.append(temp.right)
        return 0

    def __repr__(self):
        return repr(self.root)


if __name__ == '__main__':

    bst = BinarySearchTree()

### oppgave 2 ###
    # bst.insert(7)
    # bst.insert(4)
    # bst.insert(13)
    # bst.insert(2)

    # bst.insert(6)
    # bst.insert(9)
    # bst.insert(15)
    # bst.insert(1)

    # bst.insert(5)
    # bst.insert(8)
    # bst.insert(11)
    # bst.insert(12)

    # print(bst.root)

    # bst.delete(1)
    # bst.delete(11)
    # bst.delete(4)
    # bst.delete(7)

    # print(bst.root)

### oppgave 3 ###

    file = open('random_numbers.txt', 'r')
    lines = file.readlines()

    num_list = []
    for line in lines:
        bst.insert((int(line)))
        num_list.append(int(line))

    print("Level in tree of number on row 1 in the text file:")
    print(bst.level(num_list[0]))
    print("Level in tree of number on row 10 in the text file:")
    print(bst.level(num_list[9]))
    print("Level in tree of number on row 100 in the text file:")
    print(bst.level(num_list[99]))
    print("Level in tree of number on row 1000 in the text file:")
    print(bst.level(num_list[999]))
    print("Level in tree of number on row 10000 in the text file:")
    print(bst.level(num_list[9999]))
    print("Level in tree of number on row 100000 in the text file:")
    print(bst.level(num_list[99999]))
