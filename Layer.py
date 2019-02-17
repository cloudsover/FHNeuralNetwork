from FFBPNeurode import *
from DLLNode import *
from LayerType import *


class Layer(DLLNode):
    """
    This class is an extension of the DLLNode class.

    Adds functionality by integrating the FFBPNeurode into its data storage.
    Intended to be used by LayerList class to manage different layers in the
    neural network.

    Attributes:
        my_type: LayerType classification of the Layer
        neurodes: list of FFBPNeurodes contained within the layer

    """

    def __init__(self, num_neurodes: int = 5,
                 my_type: LayerType = LayerType.HIDDEN):
        """
        Inits Layer class with all attributes initialized.

        Args:
            num_neurodes: number of neurodes to initialize in the neurodes list
            my_type: LayerType classification for the layer
        """
        super().__init__()
        self.my_type = my_type
        self.neurodes = []
        self.name = random.randint(0,100)

        self.init_neurodes(num_neurodes)

    def init_neurodes(self, num_neurodes):
        """
        Helper function which initializes the self.neurodes list object

        Args:
            num_neurodes: number of FFBPNeurodes to add to the neurodes list
        """
        for i in range(num_neurodes):
            self.add_neurode()

    def add_neurode(self):
        """Adds a single FFBPNeurode to the neurodes list"""
        new_node = FFBPNeurode(self.my_type)
        self.neurodes.append(new_node)

    def get_my_neurodes(self) -> list:
        """
        Getter Function which returns the neurodes class attribute list

        Returns:
            neurodes list
        """
        return self.neurodes

    def get_layer_info(self) -> tuple:
        """
        Getter Function which returns a tuple containing the my_type
        LayerType classification of the Layer and the number of FFBPNeurodes
        in the neurodes list

        Returns:
            tuple containing my_type and len(neurodes)
        """
        return self.my_type, len(self.neurodes)
