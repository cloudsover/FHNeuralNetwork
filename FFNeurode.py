from math import e
from LayerType import LayerType
from Neurode import Neurode


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

    def receive_input(self, from_node: Neurode = None, input_value: float = 0):
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
            for neurode in self.output_nodes:
                self.receive_input(neurode)

                # If Neurode type is Output or Hidden type
        elif self.my_type is LayerType.OUTPUT or LayerType.HIDDEN:
            if self.register_input(from_node):
                self.fire()

    def register_input(self, from_node: Neurode) -> bool:
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
            self.reporting_inputs = 0
            return True
        return False

    def fire(self):
        """
        This method calculates and reports the value of the neurode based on
        the values of the input connections.

        Calculates the weighted sum of values from connected input nodes
        and their weights using the activate_sigmoid() function.

        After calculating the value of the neurode, this method reports to
        all output connected neurodes letting them known that this neurode
        has a value ready.
        """

        weighted_sum = 0

        for index, neurode in enumerate(self.input_nodes):
            weighted_sum += neurode.get_value() * self.input_nodes.get(index)
        self.value = self.activate_sigmoid(weighted_sum)

        # Pass values to output nodes
        for node in self.output_nodes:
            node.receive_input(self)
