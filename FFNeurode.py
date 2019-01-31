from LayerType import LayerType
from Neurode import Neurode
from math import e


class FFNeurode(Neurode):
    """
    This class extends the functionality of the Neurode class.

    - Accepts data from input side.
    - Processes the data and calculates it's own value.
    - 'fires' when appropriate, passing data to the output side.
    """

    def __init__(self):
        """Init method which initializes the FFNeurode class"""
        super().__init__()

    @staticmethod
    def activate_sigmoid(value) -> float:
        """
        Sigmoid function which calculates the weighted sum of the input
        values and limits the results to a value between -1 and 1

        Args:
             value: summation of input weights
        Returns:
            Float value between -1 and 1
        """
        return 1 / (1 + e ** (-value))

    def receive_input(self, from_node=None, input_value=0):
        """
        Input processing method which has different functionality
        depending on the classification of the Neurode.

        Input layer nodes:
        This method calls the receive_input() function on each neurode
        listed in the output_nodes dictionary.

        Hidden layer nodes:
        This method does not actually receive information in this case;
        simply recording that the input connection has data available by
        calling the register_input function. If register_input responds that
        all nodes are full, this method calls fire().

        Output layer nodes:
        Same as the Hidden layer.

        Args:
            from_node: node which is sending input value.

            input_value: input value given to receive.
        """

        # If Neurode type is Input type
        if self.my_type is LayerType.INPUT:
            self.value = input_value
            [self.receive_input(neurode) for neurode in self.output_nodes]

        # TODO fix this
        # If Neurode type is Output or Hidden type
        elif self.my_type is LayerType.OUTPUT or LayerType.HIDDEN:
            if self.register_input(from_node):
                self.fire()

    def register_input(self, from_node) -> bool:
        """
        This method updates the binary encoding and checks if all inputs are
        reporting.

        Using the binary encoding of reporting_inputs, we use the index of
        from_node in the input_nodes ordered dictionary to determine the bit
        position of the binary encoding to change to '1'. Once updated,
        this methood checks if all inputs are reporting. If all inputs are
        reporting, this method returns True; if all inputs are not
        reporting, this method returns False.

        Args:
            from_node: given node.

        Return:
            Boolean value, true if reporting_inputs is full, false if it is
            not.
        """

        index = list(self.input_nodes.keys()).index(from_node)
        self.reporting_inputs = self.reporting_inputs | 2 ** index

        if self.reporting_inputs == self.compare_inputs_full:
            return True
        else:
            return False

    def fire(self):
        """
        This method calculates and reports the value of the neurode based on
        the values of the input connections.

        TODO detail steps.
        After calculating the value of the neurode, this method reports to
        all output connected neurodes letting them known that this neurode
        has a value ready.
        """

        # TODO Calculate the value of the neurode based on the values of
        #  input connections, and let all the output connection neurodes
        #  know that our neurode has a value ready
        pass

    pass
