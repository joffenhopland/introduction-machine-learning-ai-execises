### exercise 1 ###
# Write a program that asks the user to enter an equation expression in a prefix notation,
# and then displays the expression in infix and postfix notation and calculates the result of the expression.
# For example:
# Please enter a prefix expression: + + * 4 5 6 7
# The infix form is: (((4 * 5) + 6) + 7)
# The postfix form is: 4 5 * 6 + 7 +
# The result is: 33


from queue import SimpleQueue
from graphviz import Digraph


class MyBinaryNode:
    def __init__(self, value, lefttree=None, righttree=None):
        self.value = value
        self.left = lefttree
        self.right = righttree

    def value(self):
        return self.value

    def left(self):
        return self.left

    def set_left(self, left):
        self.left = left

    def right(self):
        return self.right

    def set_right(self, right):
        self.right = right

    def __eq__(self, node):
        if node == None:
            return False
        elif not isinstance(node, MyBinaryNode):
            raise Exception("Equality are only for objects of equal types")
        else:
            return self.value == node.value

    def __str__(self):
        return str(self.value)

    # def __str__(self):
    #     retval = str(self.value) + " : ( "
    #     if self.left:
    #         retval += self.left.value
    #     else:
    #         retval += "none"
    #     retval += ", "
    #     if self.right:
    #         retval += self.right.value
    #     else:
    #         retval += "none"
    #     return retval + ")"

    # hjelpefunksjon for å lage en "unik" id for dot/graphviz oppsett
    def get_id(self):
        return str(id(self))

    def has_right(self):
        return self.right != None

    def has_left(self):
        return self.left != None

    def info(self):
        retval = str(self.value) + " : ( "
        if isinstance(self.left, MyBinaryNode):
            retval += str(self.left.value)
        else:
            retval += "none"
        retval += ", "
        if isinstance(self.right, MyBinaryNode):
            retval += str(self.right.value) + " )"
        else:
            retval += "none )"
        return retval

    # methods for traversing
    def traverse_prefix(self):
        print(self, '', end='')
        if self.has_left():
            self.left.traverse_prefix()
        if self.has_right():
            self.right.traverse_prefix()

    def traverse_inorder(self):
        if self.has_left():
            print('(', end='')
            self.left.traverse_inorder()
        print(self, end='')
        if self.has_right():
            self.right.traverse_inorder()
            print(')', end='')

    def traverse_postfix(self):
        if self.has_left():
            self.left.traverse_postfix()
        if self.has_right():
            self.right.traverse_postfix()
        print(self, '', end='')

    def traverse_level_order(self):
        FIFOQueue = SimpleQueue()
        FIFOQueue.put(self)
        self.level_order(FIFOQueue)
        while not FIFOQueue.empty():
            node = FIFOQueue.get()
            print(node, '', end='')

    def level_order(self, queue):
        if queue.empty():
            return
        node = queue.get()
        print(node, '', end='')
        if node.has_left():
            queue.put(node.left)
        if node.has_right():
            queue.put(node.right)
        if node.has_left() or node.has_right():
            self.level_order(queue)

    # methods to turn input string into a binary tree structure
    def parse_prefix_input(self, input_list):
        if not input_list:
            return
        self.value = input_list.pop(0)
        if not self.is_operator():
            self.value = int(self.value)
            return
        if not self.has_left() and input_list:
            self.left = MyBinaryNode(None)
            self.left.parse_prefix_input(input_list)
        if not self.has_right() and input_list:
            self.right = MyBinaryNode(None)
            self.right.parse_prefix_input(input_list)

    def is_operator(self):
        return self.value in ["+", "-", "*", "/"]

    # compute the expression
    def compute(self):
        def eval(value1, value2):
            if self.value == "+":
                return value1 + value2
            if self.value == "-":
                return value1 - value2
            if self.value == "*":
                return value1 * value2
            if self.value == "/":
                return value1 / value2
            else:
                return float('nan')
        leftVal = None
        rightVal = None
        if self.has_left():
            leftVal = self.left.compute()
        if self.has_right():
            rightVal = self.right.compute()
        if leftVal is None and rightVal is None:
            return self.value
        else:
            return eval(leftVal, rightVal)

    # method for visualizing the tree
    def visualize(self):
        def make_dot(tree, dot=None):
            if dot is None:
                dot = Digraph()
                dot.node(name=tree.get_id(), label=str(tree.value))

            if tree.has_left():
                dot.node(name=tree.left.get_id(), label=str(tree.left.value))
                dot.edge(tree.get_id(), tree.left.get_id())
                dot = make_dot(tree.left, dot)

            if tree.has_right():
                dot.node(name=tree.right.get_id(), label=str(tree.right.value))
                dot.edge(tree.get_id(), tree.right.get_id())
                dot = make_dot(tree.right, dot)

            return dot
        dot = make_dot(self)

        return dot


def make_tree(input):
    args = input.split()
    rootNode = MyBinaryNode(None)
    rootNode.parse_prefix_input(args)
    return rootNode


if __name__ == "__main__":
    the_input = input("Please enter a prefix expression: ")
    print("Thank you\n")

    tree = make_tree(the_input)

    print("The infix form is: ", end='')
    tree.traverse_inorder()
    print("\nThe postfix form is: ", end='')
    tree.traverse_postfix()
    print(f"\nThe result is: {tree.compute()}")
    tree.visualize()


# leftNode = MyBinaryNode('+', MyBinaryNode('a'), MyBinaryNode('b'))
# rightNode = MyBinaryNode('-', MyBinaryNode('a'), MyBinaryNode('b'))
# rootNode = MyBinaryNode('x', leftNode, rightNode)

# print(leftNode)
# print(rightNode)
# print(rootNode)

# print(rootNode.traverse_prefix())
# print(rootNode.traverse_inorder())
# print(rootNode.traverse_postfix())
# print(rootNode.traverse_level_order())
