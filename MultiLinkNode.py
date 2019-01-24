from abc import *
from enum import Enum, auto


class MultiLinkNode(ABC):
    """TODO DOCS"""

    def __init__(self):
        """TODO DOCS"""

        # TODO reporting_inputs
        # TODO reporting_outputs
        # TODO compare_inputs_full
        # TODO compare_outputs_full
        # TODO input_nodes
        # TODO output_nodes
        pass

    # fixme
    @abstractmethod
    def process_new_input_node(self, node):
        """TODO Docs"""
        pass

    # fixme
    @abstractmethod
    def process_new_output_node(self, node):
        """TODO DOCS"""
        pass

    # fixme
    def clear_and_add_input_node(self, nodes):
        """TODO DOcs"""
        # TODO Break this up with helper methods
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
        # TODO value
        # TODO my_type

    pass