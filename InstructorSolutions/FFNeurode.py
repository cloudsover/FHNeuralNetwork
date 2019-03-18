import numpy as np

from InstructorSolutions.MultiLinkNode import LayerType
from InstructorSolutions.Neurode import Neurode


class FFNeurode(Neurode):

    def __init__(self, my_type):
        super().__init__(my_type)

    @staticmethod
    def activate_sigmoid(value):
        return 1 / (1 + np.exp(-value))

    def register_input(self, from_node):
        self.reporting_inputs = self.reporting_inputs | (
                    2 ** list(self.input_nodes.keys()).index(from_node))
        if self.reporting_inputs == self.compare_inputs_full:
            self.reporting_inputs = 0
            return True
        else:
            return False

    def receive_input(self, from_node=None, input_value=0):
        if self.my_type is LayerType.INPUT:
            self.value = input_value
            for key in self.output_nodes:
                key.receive_input(self)
        elif self.register_input(from_node):
            self.fire()

    def fire(self):
        input_sum = 0
        for key, node_data in self.input_nodes.items():
            input_sum += key.get_value() * node_data
        self.value = FFNeurode.activate_sigmoid(input_sum)
        for key in self.output_nodes:
            key.receive_input(self)
