from collections import namedtuple
from BinaryTreeNode import BinaryTreeNode
from BinaryTree import BinaryTree
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


def test_init():
    tree = BinaryTree()
    assert tree._root == None


def test_root():
    tree = BinaryTree()
    tree.insert(value=person3)
    tree.insert(value=person2)
    tree.insert(value=person4)
    tree.insert(value=person1)
    tree.insert(value=person5)
    assert tree._root.value == person3


def test_findLeftMost():
    tree = BinaryTree()
    tree.insert(value=person3)
    tree.insert(value=person2)
    tree.insert(value=person4)
    assert tree.findLeftMost(tree._root).value == person2
    tree.insert(value=person1)
    assert tree.findLeftMost(tree._root).value == person1


def test_findRightMost():
    tree = BinaryTree()
    tree.insert(value=person3)
    tree.insert(value=person2)
    tree.insert(value=person4)
    assert tree.findRightMost(tree._root).value == person4
    tree.insert(value=person1)
    tree.insert(value=person5)
    assert tree.findRightMost(tree._root).value == person5


# maybe test more on insert??
def test_insert():
    tree = BinaryTree()
    tree.insert(value=person3)
    assert tree._root.value == person3


def test_findMin():
    tree = BinaryTree()
    tree.insert(value=person1)
    tree.insert(value=person5)
    assert tree.findMin().value == person1


def test_findMax():
    tree = BinaryTree()
    tree.insert(value=person1)
    tree.insert(value=person5)
    assert tree.findMax().value == person5


def test_find():
    tree = BinaryTree()
    assert tree.find(person1) == None
    tree.insert(value=person3)
    tree.insert(value=person2)
    tree.insert(value=person4)
    tree.insert(value=person1)
    tree.insert(value=person5)
    assert tree.find(person1).value == person1
    assert tree.find(person3).value == person3
    assert tree.find(person5).value == person5

# Er det en bedre måte å teste deleteMin og deleteMax på???


def test_deleteMin():
    tree = BinaryTree()
    tree.insert(value=person3)
    tree.insert(value=person4)
    assert tree.findMin().value == person3
    tree.deleteMin()
    tree.insert(value=person2)
    tree.insert(value=person1)
    tree.insert(value=person5)
    assert tree.findMin().value == person1
    tree.deleteMin()
    assert tree.findMin().value == person2


def test_deleteMax():
    tree = BinaryTree()
    tree.insert(value=person3)
    tree.insert(value=person2)
    tree.insert(value=person4)
    tree.insert(value=person1)
    tree.insert(value=person5)
    assert tree.findMax().value == person5
    tree.deleteMax()
    assert tree.findMax().value == person4


# hvordan teste at det blir error når man skal finne noden man har slettet?
def test_delete():
    tree = BinaryTree()
    tree.insert(value=person3)
    tree.delete(person3)
    tree.insert(value=person3)
    tree.insert(value=person2)
    tree.insert(value=person4)
    tree.insert(value=person1)
    tree.insert(value=person5)
    assert tree.find(person3).value == person3
    tree.delete(person3)
