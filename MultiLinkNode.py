from abc import ABC, abstractmethod
from collections import OrderedDict

from Neurode import *


class MultiLinkNode(ABC):
    """
    Abstract class which sets up the framework for different types of nodes
    to be used in the neural network.

    Attributes:
        input_connections: int representing the number of current input
          connections the node has

        output_connections: int representing the number of current output
          connections the node has

        reporting_inputs: binary-encoded representation of input nodes which
          have provided input to this node

        reporting_outputs: binary-encoded representation of output nodes which
          have provided input to this node

        compare_inputs_full: binary-encoded representation of all input nodes
          reporting 'full' to be used to compare against reporting_inputs

        compare_outputs_full: binary-encoded representation of all ouput nodes
          reporting 'full' to be used to compare against reporting_outputs

        input_nodes: Ordered dictionary of input nodes and corresponding
          their weights

        output_nodes: Ordered dictionary of input nodes and corresponding
          their weights
    """

    def __init__(self):
        """Inits MultiLinkNode with all class attributes initialized."""

        self.input_connections: int = 0  # number of input connections
        self.output_connections: int = 0  # number of output connections
        self.reporting_inputs: int = 0  # Binary which inputs gave info
        self.reporting_outputs: int = 0  # Binary which outputs gave info
        self.compare_inputs_full: int = 0  # Binary reported input nodes
        self.compare_outputs_full: int = 0  # Binary output nodes
        self.input_nodes: OrderedDict = OrderedDict()  # Ordered Dictionary
        self.output_nodes: OrderedDict = OrderedDict()  # Ordered Dictionary

    @abstractmethod
    def process_new_input_node(self, node):
        """
        Abstract method used to process input nodes

        Args:
            node: node object to be processed
        """

    @abstractmethod
    def process_new_output_node(self, node):
        """
        Abstract method used to process output nodes

        Args:
            node: node object to be processed
        """

    def clear_and_add_input_nodes(self, nodes: list):
        """
        Method which clears the current input nodes and connects the new
        list of nodes given.

        Clears input_nodes.
        Sets input_connections to 0.
        Sets reporting_inputs to 0.
        Sets the input_nodes dictionary to the given list of nodes with key
          values set to None.

        Args:
            nodes: list of nodes to be added
        """

        self.input_nodes.clear()
        self.input_connections = 0
        self.reporting_inputs = 0

        for index, node in enumerate(nodes):
            self.input_nodes[nodes[index]] = None
            self.process_new_input_node(nodes[index])
            self.input_connections += 1
            # self.reporting_inputs = self.reporting_inputs | 2 ** node
            self.compare_inputs_full = \
                self.compare_inputs_full | 2 ** index

    def clear_and_add_output_nodes(self, nodes: list):
        """
        Method which clears the current output nodes and connects the new
        list of nodes given.

        Clears output_nodes.
        Sets output_connections to 0.
        Sets reporting_outputs to 0.
        Sets the output_nodes dictionary to the given list of nodes with key
          values set to None.

        Args:
            nodes: list of nodes to be added
            """

        self.output_nodes.clear()
        self.output_connections = 0
        self.reporting_outputs = 0

        for index, node in enumerate(nodes):
            self.output_nodes[nodes[index]] = None
            self.process_new_output_node(nodes[index])
            self.output_connections += 1
            # self.reporting_outputs = self.reporting_outputs | 2 ** node
            self.compare_outputs_full = \
                self.compare_outputs_full | 2 ** index


def main():
    try:
        bad_instance = MultiLinkNode()
        print(
            "Error: perhaps the abstract methods were not coded correctly in MultiLinkNode")
    except TypeError:
        pass
    inodes = []
    hnodes = []
    onodes = []
    for k in range(3):
        inodes.append(Neurode(LayerType.INPUT))
    for k in range(4):
        hnodes.append(Neurode(LayerType.HIDDEN))

    onodes.append(Neurode(LayerType.OUTPUT))
    for node in inodes:
        node.clear_and_add_output_nodes(hnodes)
    for node in hnodes:
        node.clear_and_add_input_nodes(inodes)
        node.clear_and_add_output_nodes(onodes)
    for node in onodes:
        node.clear_and_add_input_nodes(hnodes)
    onodes[0].value = 10
    node_1 = list(inodes[2].output_nodes.items())[1][0]
    node_2 = list(node_1.output_nodes.items())[0][0]
    try:
        assert inodes[0].get_type() == LayerType.INPUT
        assert hnodes[0].get_type() == LayerType.HIDDEN
        assert onodes[0].get_type() == LayerType.OUTPUT
    except:
        print("Error: perhaps LayerType labels were not applied correctly")
    try:
        assert node_2.get_value() == 10
        assert 0 <= list(node_2.input_nodes.items())[1][1] < 1
        inodes[2].value = 15
        node_1 = list(onodes[0].input_nodes.items())[1][0]
        node_2 = list(node_1.input_nodes.items())[2][0]
        assert node_2.get_value() == 15
    except:
        print(
            "Error: perhaps there is a problem linking the nodes, or with get_value()")
    try:
        assert hnodes[1].compare_inputs_full == 7
        assert inodes[0].compare_outputs_full == 15
    except:
        print(
            "Error: perhaps there is an error encoding inputs_full references")


if __name__ == "__main__":
    main()
