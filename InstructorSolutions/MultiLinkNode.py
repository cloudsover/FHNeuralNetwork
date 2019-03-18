from abc import ABC, abstractmethod
import collections
from enum import Enum


# Perhaps learning rate should be a variable in the network
class LayerType(Enum):
    INPUT = 0
    OUTPUT = 1
    HIDDEN = 2


class MultiLinkNode(ABC):

    def __init__(self):
        self.num_inputs = 0
        self.num_outputs = 0
        self.reporting_inputs = 0
        self.reporting_outputs = 0
        self.compare_inputs_full = 0
        self.compare_outputs_full = 0
        self.input_nodes = collections.OrderedDict()
        self.output_nodes = collections.OrderedDict()

    def __str__(self):
        ret_str = "-->Node " + str(id(self)) + "\n"
        ret_str = ret_str + "   Input Nodes:\n"
        for key in self.input_nodes:
            ret_str = ret_str + "   " + str(id(key)) + "\n"
        ret_str = ret_str + "   Output Nodes\n"
        for key in self.output_nodes:
            ret_str = ret_str + "   " + str(id(key)) + "\n"
        return ret_str

    @abstractmethod
    def process_new_input_node(self, node):
        pass

    @abstractmethod
    def process_new_output_node(self, node):
        pass

    def add_input_node(self, node):
        self.input_nodes[node] = None
        self.process_new_input_node(node)
        self.num_inputs += 1
        self.compare_inputs_full = 2 ** self.num_inputs - 1

    def clear_and_add_input_nodes(self, nodes):
        self.clear_inputs()
        for node in nodes:
            self.add_input_node(node)

    def clear_and_add_output_nodes(self, nodes):
        self.clear_outputs()
        for node in nodes:
            self.add_output_node(node)

    def clear_inputs(self):
        self.input_nodes = collections.OrderedDict()
        self.num_inputs = 0
        self.compare_inputs_full = 0

    def add_output_node(self, node):
        self.output_nodes[node] = None
        self.process_new_output_node(node)
        self.num_outputs += 1
        self.compare_outputs_full = 2 ** self.num_outputs - 1

    def clear_outputs(self):
        self.output_nodes = collections.OrderedDict()
        self.num_outputs = 0
        self.compare_outputs_full = 0
