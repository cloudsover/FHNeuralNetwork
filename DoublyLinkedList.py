from DLLNode import DLLNode


class DoublyLinkedList:
    """TODO Docs"""

    def __init__(self, data=None):
        """TODO Docs"""
        self.data = data
        self.current = None
        self.head = None
        self.tail = None

    def __str__(self):
        """TODO Docs"""
        ret_string = []

        for node in self:
            ret_string.append(node)
            return "->".join(ret_string)

    def __iter__(self):
        """TODO Docs"""
        node = self.head

        while node:
            yield node
            node = node.get_next()

    def __contains__(self, item):
        """TODO Docs"""

        for node in self.__iter__():
            if node == item:
                return True
        return False

    def __len__(self):
        _len = 0

        for node in self.__iter__():
            _len += 1
        return _len

    def reset_cur(self):
        """TODO Docs"""
        self.current = self.head
        return self.current

    def is_empty(self):
        """TODO Docs"""
        return self.head.get_next() is None

    def add_to_head(self, node):
        """TODO Docs"""
        if self.head is None:
            self.head = self.tail = node

        temp_node = self.head
        node.set_next(temp_node)
        temp_node.set_prev(node)
        self.head = node

    def add_to_tail(self, input_node):
        """TODO Docs"""
        if self.head is None:
            self.tail = self.head = input_node

        for node in self:
            first_node = node.get_next()

            if first_node is None:
                node.set_next(input_node)
                input_node.set_prev(node)
                return

    def remove_from_head(self):
        """TODO Docs"""
        if self.head is None:
            return

        node = self.head
        next_node = node.get_next()
        next_node.set_prev(None)
        self.head = next_node

        return node

    def remove_from_tail(self):
        """TODO Docs"""
        if self.tail is None:
            return

        ret_node = self.tail

        for node in self:
            next_node = node.get_next()
            prev_node = node.get_prev()

            if next_node is None:
                prev_node.set_next(None)
                break

        return ret_node

    def insert_after_cur(self, node):
        """TODO Docs"""
        if self.current:
            node.set_next(self.current.get_next())
            self.current.set_next(node)
            return True
        else:
            return False

    def remove_after_cur(self):
        """TODO Docs"""
        if not self.current or self.current.get_next():
            return False
        else:
            self.current.set_next(self.current.get_next().get_next())

    def iterate(self):
        """TODO Docs"""
        self.current = self.current.get_next()
        return self.current

    def rev_iterate(self):
        """TODO Docs"""
        self.current = self.current.get_prev()
        return self.current


def main():
    testlist = DoublyLinkedList()
    print("Testing initial state of DoublyLinkedList")
    assert testlist.head is None
    assert testlist.tail is None
    assert testlist.current is None
    nodelist = []
    for i in range(0, 5):
        temp = DLLNode()
        nodelist.append(temp)
        print(nodelist)
    print("Test add first node to head and reset current")
    testlist.add_to_head(nodelist[0])
    testlist.reset_cur()
    assert testlist.head is nodelist[0]
    assert testlist.tail is nodelist[0]
    assert testlist.current is nodelist[0]
    assert testlist.current.get_next() is None
    assert testlist.current.get_prev() is None
    print("Test add another node to head")
    testlist.add_to_head(nodelist[1])
    assert testlist.head is nodelist[1]
    assert testlist.tail is nodelist[0]
    assert testlist.current is nodelist[0]
    assert testlist.current.get_next() is None
    assert testlist.current.get_prev() is nodelist[1]
    assert testlist.head.get_next() is nodelist[0]
    assert testlist.head.get_prev() is None
    print("Test insert after current (should add to tail)")
    testlist.insert_after_cur(nodelist[2])
    assert testlist.tail is nodelist[2]
    assert nodelist[2].get_next() is None
    assert nodelist[2].get_prev() is nodelist[0]
    assert nodelist[0].get_next() is nodelist[2]
    assert nodelist[0].get_prev() is nodelist[1]
    print("Test reset and insert current")
    testlist.reset_cur()
    testlist.insert_after_cur(nodelist[3])
    assert testlist.tail is nodelist[2]
    assert testlist.head is nodelist[1]
    assert nodelist[1].get_next() is nodelist[3]
    assert nodelist[1].get_prev() is None
    assert nodelist[0].get_next() is nodelist[2]
    assert nodelist[0].get_prev() is nodelist[3]
    assert nodelist[3].get_next() is nodelist[0]
    assert nodelist[3].get_prev() is nodelist[1]
    print("Test remove from head")
    testlist.remove_from_head()
    assert testlist.tail is nodelist[2]
    assert testlist.head is nodelist[3]
    assert nodelist[3].get_next() is nodelist[0]
    assert nodelist[3].get_prev() is None
    print("Test iterate and rev_iterate")
    assert testlist.reset_cur() == nodelist[3]
    assert testlist.iterate() == nodelist[0]
    assert testlist.iterate() == nodelist[2]
    assert testlist.rev_iterate() == nodelist[0]
    assert testlist.tail is nodelist[2]
    assert testlist.current is nodelist[0]
    print("Test remove after cur, removing tail")
    testlist.remove_after_cur()
    assert testlist.tail is nodelist[0]
    assert nodelist[0].get_next() is None
    print("Test remove after cur, nothing to remove")
    assert testlist.remove_after_cur() is False
    print("Test remove from head three times, last time should fail")
    assert testlist.remove_from_head()
    assert testlist.head is nodelist[0]
    assert testlist.tail is nodelist[0]
    assert testlist.remove_from_head()
    assert not testlist.remove_from_head()
    assert testlist.head is None
    assert testlist.tail is None


main()
