from FFBPNeurode import *
from DLLNode import *
from LayerType import *


class Layer(DLLNode):
    """TODO Docs"""

    def __init__(self, num_neurodes: int = 5,
                 my_type: LayerType = LayerType.HIDDEN):
        """TODO Docs"""
        super().__init__()
        self.my_type = my_type
        self.neurodes = []
        self.init_neurodes(num_neurodes)

    def init_neurodes(self, num_neurodes):
        """TODO Docs"""
        for i in range(num_neurodes):
            self.add_neurode()

    def add_neurode(self):
        """TODO Docs"""
        new_node = FFBPNeurode(self.get_layer_info())
        self.neurodes.append(new_node)

    def get_my_neurodes(self) -> list:
        """TODO Docs"""
        return self.neurodes

    def get_layer_info(self) -> LayerType:
        """TODO Docs"""
        return self.my_type

