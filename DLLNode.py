class DLLNode:
    """
    Double Linked List Node

    Attributes:
        next: Double Linked List node further down the line (towards tail)
        prev: Double Linked List node previous in line (towards head)
    """

    def __init__(self):
        """Inits DLLNode with all class attributes initialized."""

        self.next = None
        self.prev = None

    def __str__(self):
        """Stringizer Method"""
        return "(DLL Note)"

    def set_next(self, next_node):
        """
        Setter Function for next attribute.

        Args:
            next_node: node which to set as self.next
        """
        self.next = next_node

    def get_next(self):
        """
        Getter Function for next attribute.

        Return:
            next attribute
        """
        return self.next

    def set_prev(self, prev_node):
        """
        Setter Function for prev attribute.

        Args:
            prev_node: node which to set as self.prev
        """
        self.prev = prev_node

    def get_prev(self):
        """
        Getter function for prev attribute.

        Return:
            prev attribute
        """
        return self.prev
