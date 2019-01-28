from LayerType import LayerType
from Neurode import Neurode
from math import e


class FFBPNeurode(Neurode):
    """TODO Docs"""

    def __init__(self):
        """TODO Docs"""
        super().__init__()

    @staticmethod
    def activate_sigmoid(value):
        """
        Sigmoid function which calculates the weighted sum of the input
        values and limits the results to a value between -1 and 1

        Args:
             value: summation of input weights
        Returns:
            Float value between -1 and 1
        """
        return 1 / (1 + e ** (-value))

    def receive_input(self, from_node=None, input_value=0):
        """TODO Docs"""

        # TODO fix this
        if self.my_type is LayerType.INPUT:
            pass

        # TODO fix this
        if self.my_type is LayerType.OUTPUT:
            pass

        # TODO fix this
        if self.my_type is LayerType.HIDDEN:
            pass

        pass

    def register_input(self, from_node):
        """TODO Docs"""

        # TODO Update binary encoding reporting_inputs
        #      Use the index of from_node in input_nodes
        #      to determine which bit position to change to 1

        # TODO Check if all inputs are reporting ( use the ref value )

        # TODO If all inputs are reporting, reset reporting_inputs to 0 and
        #  return true. Else return False

        pass

    def fire(self):
        """TODO Docs"""

        # TODO Calculate the value of the neurode based on the values of
        #  input connections, and let all the output connection neurodes
        #  know that our neurode has a value ready
        pass

    pass
