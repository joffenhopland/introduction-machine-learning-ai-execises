class MyNode:
    def __init__(self, value, next=None, prev=None):
        self.value = value
        self.next = next
        self.prev = prev

    def __str__(self):
        return str(self.value)

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def get_prev(self):
        return self.prev

    def set_prev(self, node):
        self.prev = node

    def get_next(self):
        return self.next

    def set_next(self, node):
        self.next = node


class MyLinkedList:
    def __init__(self, data=None):
        self.first = None
        self.current = None
        self.last = None
        self.size = 0

        if data is not None:
            if hasattr(data, '__iter__'):
                for item in data:
                    self.append(item)
            else:
                self.append(data)

    def __getitem__(self, idx):
        if idx >= self.size or idx < 0:
            raise IndexError
        current_node = self.first
        current_i = 0

        while current_i < idx:
            print(current_i, " - ", current_node.get_value())
            current_node = current_node.get_next()
            current_i += 1
        return current_node.get_value()

    def __setitem__(self, idx, item):
        current_node = self.first
        current_i = 0

        while current_i < idx:
            current_node = current_node.get_next()
            current_i += 1

        current_node.set_value(item)

    def __add__(self, list):
        newlist = MyLinkedList()

        for item in self:
            newlist.append(item)
        for item in list:
            newlist.append(item)
        return newlist

    def __delitem__(self, idx):
        if idx >= self.size or idx < 0:
            raise IndexError

        if idx == 0:  # handle first element
            self.first = self.first.get_next()
            self.first.set_prev(None)
        elif idx == self.size - 1:  # handle last element
            self.last = self.last.get_prev()
            self.last.set_next(None)
        else:
            current_node = self.first
            current_i = 0

            while current_i < idx:
                current_node = current_node.get_next()
                current_i += 1

            current_node.get_prev().set_next(current_node.get_next())
            current_node.get_next().set_prev(current_node.get_prev())
        self.size -= 1

    def __eq__(self, list):
        if self.size != list.size:
            return False

        for i in range(self.size):
            if self[i] != list[i]:
                return False
        return True

    def __iter__(self):
        self.current = self.first
        return self

    def __next__(self):
        if self.current is None:
            raise StopIteration
        else:
            current_n = self.current
            self.current = self.current.get_next()
            return current_n.get_value()

    def __len__(self):
        return self.size

    def __contains__(self, item):
        current_node = self.first

        while True:
            if current_node.get_value() == item:
                return True
            current_node = current_node.get_next()
            if (current_node is None):
                break
        return False

    def __str__(self):
        result = ""
        if self.size > 0:
            current_node = self.first
            while True:
                result += str(current_node) + ", "
                current_node = current_node.get_next()
                if (current_node is None):
                    break
        return result

    def append(self, item):
        # Append an item at the end of the list.
        if self.first is None:
            self.first = MyNode(item)
            self.last = self.first
        else:
            self.last.set_next(MyNode(item, self.last))
            self.last = self.last.get_next()
        self.size += 1

    def insert(self, idx, item):
        if idx >= self.size or idx < 0:
            raise IndexError
        new_node = MyNode(item)

        if idx == 0:
            new_node.set_next(self.first)
            self.first.set_prev(new_node)
            self.first = new_node
        else:
            current_node = self.first
            current_i = 0

            while current_i < idx:
                current_node = current_node.get_next()
                current_i += 1

            current_node.get_prev().set_next(new_node)
            new_node.set_next(current_node)
            new_node.set_prev(current_node.get_prev())
            current_node.set_prev(new_node)
        self.size += 1


class MyStack(MyLinkedList):
    def __init__(self, data=None):
        super().__init__(data)

    def push(self, data):
        self.append(data)

    def top(self):
        return self.last.get_value()

    def peek(self):
        return self.top()

    def pop(self):
        if (self.last is None):
            raise IndexError

        value = self.last.get_value()
        if self.last.get_prev() is not None:
            self.last = self.last.get_prev()
            self.last.set_next(None)
        else:  # we have reached the first element
            self.last = None
            self.first = None

        self.size -= 1
        return value


class MyFIFO(MyLinkedList):
    def __init__(self, data=None):
        super().__init__(data)

    def enqueue(self, data):
        self.append(data)

    def dequeue(self):
        if (self.first is None):
            raise IndexError

        value = self.first.get_value()
        if self.first.get_next() is not None:
            self.first = self.first.get_next()
            self.first.set_prev(None)
        else:  # we have reached the first element
            self.last = None
            self.first = None

        self.size -= 1
        return value
