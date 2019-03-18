from InstructorSolutions.MultiLinkNode import LayerType
from InstructorSolutions.Neurode import Neurode


class BPNeurode(Neurode):

    def __init__(self, my_type):
        super().__init__(my_type)
        self.delta = 0
        self.learning_rate = .05

    def get_delta(self):
        return self.delta

    def get_weight_for_input_node(self, from_node):
        return self.input_nodes[from_node]

    def register_back_input(self, from_node):
        if self.my_type == LayerType.OUTPUT:
            return True
        self.reporting_outputs = self.reporting_outputs | (
                    2 ** list(self.output_nodes.keys()).index(from_node))
        if self.reporting_outputs == self.compare_outputs_full:
            self.reporting_outputs = 0
            return True
        else:
            return False

    def calculate_delta(self, expected=None):
        if self.my_type == LayerType.OUTPUT:
            error = expected - self.value
            self.delta = error * self.sigmoid_derivative(self.value)
        else:
            self.delta = 0
            for neurode, data in self.output_nodes.items():
                self.delta += neurode.get_weight_for_input_node(
                    self) * neurode.get_delta()
            self.delta *= self.sigmoid_derivative(self.value)

    def get_learning_rate(self):
        return self.learning_rate

    def adjust_input_node(self, node, value):
        self.input_nodes[node] += value

    def update_weights(self):
        for key, node_data in self.output_nodes.items():
            adjustment = key.get_learning_rate() * key.get_delta() * self.value
            key.adjust_input_node(self, adjustment)

    def receive_back_input(self, from_node, expected=None):
        if self.register_back_input(from_node):
            self.calculate_delta(expected)
            self.back_fire()
            if self.my_type is not LayerType.OUTPUT:
                self.update_weights()

    def back_fire(self):
        for key in self.input_nodes:
            key.receive_back_input(self)

    @staticmethod
    def sigmoid_derivative(value):
        return value * (1.0 - value)
