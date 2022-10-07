from collections import namedtuple
from BinaryTreeNode import BinaryTreeNode
import pytest

Person = namedtuple(
    'Person', ['etternavn', 'fornavn', 'adresse', 'postnummer', 'poststed'])

person1 = Person('AAKVIK', 'ANETTE', 'BAKLIEN 11', '1360', 'NESBRU')
person2 = Person('ALFREDSEN', 'JON REMY', 'FLESNES 59', '3738', 'SKIEN')
person3 = Person(etternavn='ELI', fornavn='RITA HELEN',
                 adresse='MEHEIAVEGEN 80', postnummer='4436', poststed='GYLAND')
person4 = Person('GJERSTAD', 'TORKJELL', 'HOSTELAND 2 83', '1361', 'ØSTERÅS')
person5 = Person('KRISTIANSEN', 'MORTEN KRISTIAN',
                 'LEINAHYTTA 36', '7224', 'MELHUS')
person6 = Person('LARSEN', 'MONSEN',
                 'STEGANE 10', '6783', 'STRYN')
person7 = Person('RAKE', 'STIAN',
                 'HAREFLATEN 12', '6796', 'HOPLAND')


def test_value():
    assert BinaryTreeNode(person1).value == person1


def test_hasLeft():
    node1 = BinaryTreeNode(person1, BinaryTreeNode(
        person2), BinaryTreeNode(person3))
    assert node1.hasLeft() == True
    node2 = BinaryTreeNode(person1)
    assert node2.hasLeft() == False


def test_hasRight():
    node1 = BinaryTreeNode(person1, BinaryTreeNode(
        person2), BinaryTreeNode(person3))
    assert node1.hasRight() == True
    node2 = BinaryTreeNode(person1)
    assert node2.hasRight() == False


def test_eq():
    n1 = BinaryTreeNode(person1)
    n2 = BinaryTreeNode(person1)
    assert n1 == n2


@pytest.mark.xfail
def test_ne():
    n1 = BinaryTreeNode(person1)
    n2 = BinaryTreeNode(person2)
    assert n1 != n2


def test_lt():
    n1 = BinaryTreeNode(person1)
    n2 = BinaryTreeNode(person2)
    assert n1 < n2


def test_le():
    n1 = BinaryTreeNode(person1)
    n2 = BinaryTreeNode(person2)
    assert n1 <= n2
    n3 = BinaryTreeNode(person3)
    n4 = BinaryTreeNode(person3)
    assert n3 <= n4


def test_gt():
    n1 = BinaryTreeNode(person1)
    n2 = BinaryTreeNode(person2)
    assert n2 > n1


def test_ge():
    n1 = BinaryTreeNode(person1)
    n2 = BinaryTreeNode(person2)
    assert n2 >= n1
    n3 = BinaryTreeNode(person3)
    n4 = BinaryTreeNode(person3)
    assert n3 >= n4


def test_prefixOrder():
    leftNode = BinaryTreeNode(person1, BinaryTreeNode(
        person2), BinaryTreeNode(person3))
    rightNode = BinaryTreeNode(person4, BinaryTreeNode(
        person5), BinaryTreeNode(person6))
    rootNode = BinaryTreeNode(person7, leftNode, rightNode)
    tree = rootNode
    print("The prefix form is: \n", end='')
    tree.prefixOrder()


def test_infixOrder():
    leftNode = BinaryTreeNode(person1, BinaryTreeNode(
        person2), BinaryTreeNode(person3))
    rightNode = BinaryTreeNode(person4, BinaryTreeNode(
        person5), BinaryTreeNode(person6))
    rootNode = BinaryTreeNode(person7, leftNode, rightNode)
    tree = rootNode
    print("\nThe infix form is: \n", end='')
    tree.infixOrder()


def test_postfixOrder():
    leftNode = BinaryTreeNode(person1, BinaryTreeNode(
        person2), BinaryTreeNode(person3))
    rightNode = BinaryTreeNode(person4, BinaryTreeNode(
        person5), BinaryTreeNode(person6))
    rootNode = BinaryTreeNode(person7, leftNode, rightNode)
    tree = rootNode
    print("\nThe postfix form is: \n", end='')
    tree.postfixOrder()


def test_levelOrder():
    leftNode = BinaryTreeNode(person1, BinaryTreeNode(
        person2), BinaryTreeNode(person3))
    rightNode = BinaryTreeNode(person4, BinaryTreeNode(
        person5), BinaryTreeNode(person6))
    rootNode = BinaryTreeNode(person7, leftNode, rightNode)
    tree = rootNode
    print("\nThe levelorder form is: \n", end='')
    tree.levelOrder()


test_prefixOrder()
test_infixOrder()
test_postfixOrder()
test_levelOrder()
