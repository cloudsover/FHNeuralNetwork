from LayerType import LayerType
from Neurode import Neurode


class BPNeurode(Neurode):
    """TODO Docs"""

    def __init__(self, my_type=LayerType.INPUT):
        """TODO Docs"""
        super().__init__(my_type)

        self.data = 0
        self.learning_rate = 0.05

    @staticmethod
    def sigmoid_derivative(value) -> float:
        """TODO Docs"""
        pass

    def receive_back_input(self, from_node: Neurode, expected: int = 0):
        """TODO Docs"""

        if from_node.my_type is LayerType.OUTPUT:
            pass

        if from_node.my_type is LayerType.HIDDEN:
            pass

        if from_node.my_type is LayerType.INPUT:
            pass
        #
        # # If Neurode type is Input type
        # if self.my_type is LayerType.INPUT:
        #     # self.value = input_value
        #     for neurode in self.output_nodes:
        #         self.receive_input(neurode)
        #
        #         # If Neurode type is Output or Hidden type
        # elif self.my_type is LayerType.OUTPUT or LayerType.HIDDEN:
        #     if self.register_input(from_node):
        #         self.fire()
        # pass

    def calculate_delta(self, expected=None):
        """TODO Docs"""
        pass

    def update_weights(self):
        """TODO Docs"""
        pass

    def back_fire(self):
        """TODO Docs"""
        pass
