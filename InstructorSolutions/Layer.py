from InstructorSolutions.DLLNode import DLLNode
from InstructorSolutions.FFBPNeurode import FFBPNeurode
from InstructorSolutions.MultiLinkNode import LayerType


class Layer(DLLNode):
    def __init__(self, num_neurodes=5, my_type=LayerType.HIDDEN):
        super().__init__()
        self.my_type = my_type
        self.neurodes = []
        for i in range(num_neurodes):
            self.add_neurode()

    def get_my_neurodes(self):
        return self.neurodes

    def add_neurode(self):
        new_neurode = FFBPNeurode(self.my_type)
        self.neurodes.append(new_neurode)

    def get_layer_info(self):
        return self.my_type, len(self.neurodes)

    def get_my_type(self):
        return self.my_type