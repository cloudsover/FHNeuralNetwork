from abc import *
from enum import Enum, auto


class MultiLinkNode(ABC):
    """TODO DOCS"""

    def __init__(self):
        """TODO DOCS"""

        # TODO reporting_inputs
        self.input_connections = None
        self.output_connections = None
        self.reporting_inputs = []  # Binary
        self.reporting_outputs = []  # Binary
        self.compare_inputs_full = []  # Binary
        self.compare_outputs_full = []  # Binary
        self.input_nodes = None  # Ordered Dictionary
        self.output_nodes = None  # Ordered Dictionary

        pass

    # fixme
    @abstractmethod
    def process_new_input_node(self, node):
        """TODO Docs"""

    # fixme
    @abstractmethod
    def process_new_output_node(self, node):
        """TODO DOCS"""

    # fixme
    def clear_and_add_input_nodes(self, nodes: list):
        """TODO DOcs"""
        # TODO Break this up with helper methods
        # TODO Clear entire dictionary of input nodes
        # - Adjusting all internal variables
        # TODO add each node in our list as a key in the input nodes dict,
        #  with a value of None.
        # TODO Run proccess_new_input_node() for each node, and again update
        #  relevant variables (compare_input_full)

        pass

    def clear_and_add_output_nodes(self, nodes: list):
        """TODO Docs"""
        # TODO duplicate code from input nodes function
        pass

    pass


class LayerType(Enum):
    """TODO DOCS"""
    INPUT = auto()
    HIDDEN = auto()
    OUTPUT = auto()


# FIXME
class Neurode(MultiLinkNode):
    """TODO DOCS"""

    def __init__(self, my_type):
        """TODO DOCS"""
        super().__init__()
        self.value = None  # current value of the Neurode
        self.my_type = my_type  # LayerType values: input, hidden, or output
        # TODO value
        # TODO my_type

    def get_value(self):
        """TODO Docs"""
        return self.value

    def get_my_type(self):
        """TODO Docs"""
        return self.my_type

    def process_new_input_node(self, node):
        """TODO DOCS"""

        # TODO generate a random number between 0 and 1
        # TODO Generate a new dictionary entry
        pass

    def process_new_output_node(self, node):
        """TODO Docs"""
        # Does nothing right now
        pass
