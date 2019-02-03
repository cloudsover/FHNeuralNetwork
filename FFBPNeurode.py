from BPNeurode import BPNeurode
from FFNeurode import FFNeurode
from LayerType import LayerType


class FFBPNeurode(BPNeurode, FFNeurode):
    """TODO Docs"""

    def __init__(self, my_type=LayerType.INPUT):
        """TODO Docs"""
        super().__init__(my_type)
