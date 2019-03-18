import random

from InstructorSolutions.MultiLinkNode import MultiLinkNode


class Neurode(MultiLinkNode):

    def __init__(self, my_type):
        super().__init__()
        self.value = 0
        self.my_type = my_type

    def process_new_input_node(self, node):
        node_data = random.random()
        self.input_nodes[node] = node_data

    def process_new_output_node(self, node):
        pass

    def get_value(self):
        return self.value

    def get_type(self):
        return self.my_type
