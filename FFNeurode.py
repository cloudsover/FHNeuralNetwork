from math import e
import numpy as np
from LayerType import LayerType
from Neurode import Neurode


class FFNeurode(Neurode):
    """
    This class extends the functionality of the Neurode class.

    - Accepts data from input side.
    - Processes the data and calculates it's own value.
    - 'fires' when appropriate, passing data to the output side.
    """

    def __init__(self, my_type: LayerType = LayerType.INPUT):
        """Init method which initializes the FFNeurode class"""
        super().__init__(my_type)

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
                neurode.receive_input(self)

        # If Neurode type is Output or Hidden type
        elif self.register_input(from_node):
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

        self.reporting_inputs = self.reporting_inputs | (
                    2 ** list(self.input_nodes.keys()).index(from_node))

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

        for index, neurode in self.input_nodes.items():
            weighted_sum += index.get_value() * neurode
        self.value = self.activate_sigmoid(weighted_sum)

        # Pass values to output nodes
        for node in self.output_nodes:
            node.receive_input(self.value)


def main():
    inodes = []
    hnodes = []
    onodes = []
    for k in range(2):
        inodes.append(FFNeurode(LayerType.INPUT))
    for k in range(2):
        hnodes.append(FFNeurode(LayerType.HIDDEN))
    onodes.append(FFNeurode(LayerType.OUTPUT))
    for node in inodes:
        node.clear_and_add_output_nodes(hnodes)
    for node in hnodes:
        node.clear_and_add_input_nodes(inodes)
        node.clear_and_add_output_nodes(onodes)
    for node in onodes:
        node.clear_and_add_input_nodes(hnodes)
    try:
        inodes[0].receive_input(None, 0)
        assert onodes[0].get_value() == 0
    except:
        print("Error: Neurodes may be firing before receiving all input")
    inodes[1].receive_input(None, 1)

    value_0 = (1 / (1 + np.exp(-hnodes[0].input_nodes[inodes[1]])))
    value_1 = (1 / (1 + np.exp(-hnodes[1].input_nodes[inodes[1]])))
    inter = onodes[0].input_nodes[hnodes[0]] * value_0 + onodes[0].input_nodes[
        hnodes[1]] * value_1
    final = (1 / (1 + np.exp(-inter)))
    try:
        assert final == onodes[0].get_value()
        assert 0 < final < 1
    except:
        print("Error: Calculation of neurode value may be incorrect")


if __name__ == "__main__":
    main()
