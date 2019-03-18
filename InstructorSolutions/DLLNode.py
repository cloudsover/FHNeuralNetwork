class DLLNode:
    """ Node class for a DoublyLinkedList - not designed for
        general clients, so no accessors or exception raising """

    def __init__(self):
        self.prev = None
        self.next = None

    def set_next(self, next_node):
        self.next = next_node

    def get_next(self):
        return self.next

    def set_prev(self, prev_node):
        self.prev = prev_node

    def get_prev(self):
        return self.prev


class DoublyLinkedList():

    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    def reset_cur(self):
        self.current = self.head
        return self.current

    def iterate(self):
        if self.current is not None:
            self.current = self.current.get_next()
        return self.current

    def rev_iterate(self):
        if self.current is not None:
            self.current = self.current.get_prev()
        return self.current

    def add_to_head(self, new_node):
        if isinstance(new_node, DLLNode):
            new_node.set_next(self.head)
            if self.head:
                self.head.set_prev(new_node)
            self.head = new_node
            if self.tail is None:
                self.tail = new_node

    def remove_from_head(self):
        if not self.head:
            return None
        ret_node = self.head
        self.head = ret_node.get_next()  # unlink
        if self.head:
            self.head.set_prev(None)
        ret_node.set_next(None)  # don't give client way in
        if self.head is None:
            self.tail = None
        return ret_node

    def insert_after_cur(self, new_node):
        if isinstance(new_node, DLLNode) and self.current:
            new_node.set_next(self.current.get_next())
            new_node.set_prev(self.current)
            if self.current.get_next():
                self.current.get_next().set_prev(new_node)
            self.current.set_next(new_node)
            if self.tail == self.current:
                self.tail = new_node
            return True
        else:
            return False

    def remove_after_cur(self):
        if not self.current or not self.current.get_next():
            return False
        else:
            if self.tail == self.current.get_next():
                self.tail = self.current
            self.current.set_next(self.current.get_next().get_next())
            if self.current.get_next():
                self.current.get_next().set_prev(self.current)
