from DLLNode import DLLNode


class DoublyLinkedList:
    """TODO Docs"""

    def __init__(self, data=None):
        """TODO Docs"""
        self.data = data
        self.current: DLLNode = None
        self.head: DLLNode = None
        self.tail: DLLNode = None

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

    def iterate(self):
        """TODO Docs"""
        self.current = self.current.get_next()
        return self.current

    def rev_iterate(self):
        """TODO Docs"""
        self.current = self.current.get_prev()
        return self.current

    def add_to_head(self, new_node):
        """TODO Docs"""
        if self.head is None:
            self.head = new_node = self.tail

        elif isinstance(new_node, DLLNode):
            new_node.set_next(self.head)
            self.head.next.set_prev(self.head)
            self.head = new_node

    def remove_from_head(self):
        """TODO Docs"""
        ret_node = self.head
        if ret_node:
            temp_node = ret_node.next.get_next()
            self.head = ret_node.get_next()
            self.head.set_prev(temp_node)
        ret_node.set_next(None)

    def insert_after_cur(self, new_node):
        """TODO Docs"""
        if isinstance(new_node, DLLNode) and self.current:
            new_node.set_next(self.current.get_next())
            if new_node is not self.head:
                self.current.next.set_prev(new_node)
            self.current.set_next(new_node)
            return True
        else:
            return False

    def remove_after_cur(self):
        if not self.current or self.current.get_next():
            return False
        else:
            return True



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
