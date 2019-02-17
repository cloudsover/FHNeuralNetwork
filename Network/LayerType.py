from enum import Enum


class LayerType(Enum):
    """
    Enum class which is used as a type-flag for different node classes.

    INPUT = Input node/layer
    HIDDEN = Hidden node/layer
    OUTPUT = Output node/layer
    """
    INPUT = 1
    HIDDEN = 2
    OUTPUT = 3
