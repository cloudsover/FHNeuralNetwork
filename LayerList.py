import NodePositionError
from Layer import *
from DoublyLinkedList import *


class LayerList(DoublyLinkedList):
    """TODO Docs"""

    def __init__(self, num_inputs: int, num_outputs: int):
        """TODO Docs"""
        super().__init__()

        self.input_layer: Layer = Layer(num_inputs, LayerType.INPUT)
        self.output_layer = Layer(num_outputs, LayerType.OUTPUT)
        pass

    def _init_list(self) -> list:
        """TODO Docs"""
        stuff = 0

    def get_input_nodes(self) -> list:
        """TODO Docs"""
        # fixme --------------------------
        return self.head.get_my_neurodes()

    def get_output_nodes(self) -> list:
        """TODO Docs"""
        # fixme --------------------------
        return self.tail.get_my_neurodes()

    def insert_after_cur(self, new_layer):
        """TODO Docs"""
        pass

    def insert_hidden_layer(self, num_neurodes: int):
        """TODO Docs"""
        if self.current is self.tail:
            raise NodePositionError
        else:
            self.insert_after_cur(Layer(num_neurodes, LayerType.HIDDEN))

    def remove_hidden_layer(self):
        """TODO Docs"""
        if self.current is self.tail or self.current is self.head:
            raise NodePositionError
        else:
            prev_nodes, next_nodes = self.link_nodes()
            LayerList.reconnect_nodes(prev_nodes, next_nodes)
            self.unlink_current()

    def unlink_current(self):
        """TODO Docs"""
        self.current.set_next(None)
        self.current.set_prev(None)
        self.reset_cur()

    def link_nodes(self):
        """TODO Docs"""
        prev_nodes = self.current.get_prev()
        next_nodes = self.current.get_next()

        self.current.get_prev().set_next(self.current.get_next())
        self.current.get_next().set_prev(self.current.get_prev())
        return prev_nodes, next_nodes

    @staticmethod
    def reconnect_nodes(prev_nodes, next_nodes):
        """TODO Docs"""
        LayerList.reconnect_inputs(next_nodes, prev_nodes)
        LayerList.reconnect_outputs(prev_nodes, next_nodes)

    @staticmethod
    def reconnect_inputs(node_layer: Layer, connect_to: Layer):
        """TODO Docs"""
        for node in node_layer.neurodes:
            node.clear_and_add_input_nodes(connect_to.neurodes)

    @staticmethod
    def reconnect_outputs(node_layer: Layer, connect_to: Layer):
        """TODO Docs"""
        for node in node_layer.neurodes:
            node.clear_and_add_output_nodes(connect_to.neurodes)
