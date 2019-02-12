class DLLNode:
    """TODO Docs"""

    def __init__(self):
        """TODO Docs"""

        self.next = None
        self.prev = None

    def __str__(self):
        """TODO Docs"""
        pass

    def set_next(self, next_node):
        """TODO Docs"""
        self.next = next_node

    def get_next(self):
        """TODO Docs"""
        return self.next

    def set_prev(self, prev_node):
        """TODO Docs"""
        self.prev = prev_node

    def get_prev(self):
        """TODO Docs"""
        return self.prev
