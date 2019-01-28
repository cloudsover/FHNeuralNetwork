from LayerType import LayerType
from Neurode import Neurode
from math import e


class FFBPNeurode(Neurode):
    """TODO Docs"""

    def __init__(self):
        """TODO Docs"""
        super().__init__()

    @staticmethod
    def activate_sigmoid(value) -> float:
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

        # If Neurode type is Input
        if self.my_type is LayerType.INPUT:
            self.value = input_value
            [self.receive_input(neurode) for neurode in self.output_nodes]

        # TODO fix this
        # If Neurode type is Output
        elif self.my_type is LayerType.OUTPUT or LayerType.HIDDEN:
            if self.register_input(from_node):
                self.fire()

    def register_input(self, from_node) -> bool:
        """TODO Docs"""

        index = list(self.input_nodes.keys()).index(from_node)
        self.reporting_inputs = self.reporting_inputs | 2 ** index

        if self.reporting_inputs == self.compare_inputs_full:
            return True
        else:
            return False

    def fire(self):
        """TODO Docs"""

        # TODO Calculate the value of the neurode based on the values of
        #  input connections, and let all the output connection neurodes
        #  know that our neurode has a value ready
        pass

    pass
