from DLLNode import DLLNode


class DoublyLinkedList:
    """
    Doubly-Linked List Data Type

    Attributes:
        current: 'pointer' node
        head: node at the 'top' of the list
        tail: node at the 'bottom' of the list
    """

    def __init__(self):
        """Inits DoublyLinkedList with all class attributes initialized."""
        self.current: DLLNode = None
        self.head: DLLNode = None
        self.tail: DLLNode = None

    def __str__(self):
        """Stringizer"""
        pass

    def iterate(self):
        """
        Iterator method which moves towards the bottom of the list one node
        at a time.

        Returns:
            current pointer node.
        """
        self.current = self.current.get_next()
        return self.current

    def rev_iterate(self):
        """
        Iterator method which moves towards the top of the list one node
        at a time.

        Returns:
            current pointer node.
        """
        self.current = self.current.get_prev()
        return self.current

    def reset_cur(self):
        """
        Method which resets the current pointer node to point at the
        head of the list

        Returns:
            current pointer node
        """
        self.current = self.head
        return self.current

    def is_empty(self):
        return self.head.get_next() is None

    def add_to_head(self, new_node):
        """
        Inserts a new node at the head of the list.

        Args:
            new_node: node to add to list
        """
        if self.head is None:
            self.head = self.tail = new_node
            self.current = self.head
            self.head.set_prev(None)
            self.tail.set_next(None)
        else:
            self.head.set_prev(new_node)
            new_node.set_next(self.head)
            self.head = new_node

    def remove_from_head(self):
        """
        Removes a node from the head of the list.

        Returns:
            node removed
        """
        if self.head is self.tail:
            ret_node = self.head
            self.head = None
            self.tail = None
            return ret_node

        ret_node = self.head
        if ret_node:
            self.head = ret_node.get_next()
            self.head.set_prev(None)
        ret_node.set_next(None)
        if self.head is None:
            self.tail = None
        return ret_node

    def insert_after_cur(self, new_node):
        """
        Inserts a node after the current pointer node.

        Args:
            new_node: node to add

        """
        if self.current is self.tail:
            new_node.set_prev(self.tail.get_prev())
            self.tail = new_node
            self.current.set_next(self.tail)
            self.tail.set_prev(self.current)

        else:
            self.current.get_next().set_prev(new_node)
            new_node.set_next(self.current.get_next())
            new_node.set_prev(self.current)
            self.current.set_next(new_node)

    def remove_after_cur(self) -> bool:
        """
        Removes the node after teh current pointer node.

        Returns:
            true if successful, false if not.
        """
        if self.current.get_next() is self.tail:
            self.tail = self.current
            self.current.set_next(None)
            self.tail.set_next(None)
            return True

        if not self.current or not self.current.get_next():
            return False

        self.current.set_next(self.current.get_next().get_next())
        self.current.next.next.set_prev(self.current)
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
