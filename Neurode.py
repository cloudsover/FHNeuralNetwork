import random
from enum import Enum

from MultiLinkNode import *
from LayerType import LayerType


class Neurode(MultiLinkNode):
    """
    Inherited Class through MultiLinkNode

    Attributes:
        value: Current value of the Neurode
        my_type: Given LayerType

    """

    def __init__(self, my_type):
        """
        Inits Neurode with all class and inherited attributes initialized

        Args:
            my_type: LayerType, which indicates the type of layer this
            neurode will be part of
        """
        super().__init__()
        self.value = 0  # current value of the Neurode
        self.my_type = my_type  # LayerType values: input, hidden, or output

    def get_value(self) -> float:
        """
        Getter method for value attribute

        Returns:
            Current value of the Neurode

        """
        return self.value

    def get_type(self) -> Enum:
        """
        Getter method for my_type attribute

        Returns:
            Current LayerType setting of my_type
        """
        return self.my_type

    def process_new_input_node(self, node: MultiLinkNode):
        """
        Method which processes a node to be added to input connections

        Generates a random weight, and then adds the node and the given
          weight to the ordered dictionary input_nodes

        Args:
            node: given node
        """
        weight = random.random()
        self.input_nodes[node] = weight

    def process_new_output_node(self, node: MultiLinkNode):
        """
        Method which processes a node to be added to output connections

        Implemented stub method
        Args:
            node: given node
        """
        pass
