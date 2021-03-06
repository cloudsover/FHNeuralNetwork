from Network.DLLNode import DLLNode

# TODO Take out getters a setters


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
        separator = " -> "
        len_separator = len(separator)

        if self.is_empty():
            return "\n[ empty list ]\n"

        ret_str = "\n[START LIST]: "
        p = self.head
        while p is not None:
            ret_str += (str(p) + separator)
            p = p.get_next()

        # remove extra "->" and add terminator
        ret_str = ret_str[:-len_separator] + "  [END LIST]\n"
        return ret_str

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

        existing_node = self.current
        remove_node = self.current.get_next()

        existing_node.set_next(remove_node.get_next())
        remove_node.get_next().set_prev(existing_node)
        return True