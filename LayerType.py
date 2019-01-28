from enum import Enum, auto


class LayerType(Enum):
    """
    Enum class which is used as a type-flag for different node classes.

    INPUT = Input node/layer
    HIDDEN = Hidden node/layer
    OUTPUT = Output node/layer
    """
    INPUT = auto
    HIDDEN = auto
    OUTPUT = auto