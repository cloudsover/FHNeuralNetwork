from LayerType import LayerType
from Neurode import Neurode


class BPNeurode(Neurode):
    """
    This class extends the functionality of the Neurode class.

    - Adds back-propagation functionality

    Attributes:
        delta: measure of how incoming weights need to change
        learning_rate: learning rate of the network
    """

    def __init__(self, my_type: LayerType = LayerType.INPUT):
        """
        Inits BPNeurode with all class and inherited attributes initialized.

        Args:
            my_type: LayerType Enum
        """
        super().__init__(my_type)

        self.delta = 0
        self.learning_rate = 0.05

    @staticmethod
    def sigmoid_derivative(value: float) -> float:
        """
        Static method which calculates the derivative at the given value.

        Args:
            value: Given value (float).

        Return:
            The calculated derivative at the given value.
        """
        return value * (1 - value)

    def receive_back_input(self, from_node, expected: float = 0):
        """
        This function collects inputs from connected neurodes
        and decides when to call back_fire().

        Hidden Layer: Will wait for all downstream (toward output) nodes to
                      calculate their deltas.  It will then calculate it's own
                      delta, update incoming weights and "back_fire".

        Output Layer: Receive_back_input() will calculate the delta,
                      "back_fire" to the neurodes in the last hidden layer,
                      and update the incoming weights.

        Args:
            from_node: node to collect input from

            expected: expected value of node

        """

        # Output Layer Node
        if self is LayerType.OUTPUT:
            self.calculate_delta(expected)
            self.back_fire()
            self.update_weights()

        # Hidden Layer Node
        if self is LayerType.HIDDEN:
            for node in self.output_nodes:
                node.calculate_delta()

            self.calculate_delta()
            self.update_weights()
            self.back_fire()

        # Input Layer Node
        if self.my_type is LayerType.INPUT:
            pass

    def register_back_input(self, from_node) -> bool:
        """
        This method updates the binary encoding and checks if all inputs
        are reporting.

        Args:
            from_node: given node.

        Return:
            Boolean value, true if reporting_inputs is full, false if it is
            not.

        """

        if self.my_type is LayerType.OUTPUT:
            return True

        index = list(self.output_nodes.keys()).index(from_node)
        self.reporting_outputs = self.reporting_outputs | 2 ** index

        if self.reporting_outputs == self.compare_outputs_full:
            self.reporting_outputs = 0
            return True
        return False

    def calculate_delta(self, expected=None):
        """
        Method which updates the delta attribute based on the layer type
        of the node. Updates the weights of incoming nodes.

        Output Layer Node:
         delta for output neurode = (expected value - value) *
                                     sigmoid_derivative

        Hidden Layer Node:
         weighted deltas = sum(weight of self node logged by target node *
                           delta of target node) delta for hidden neurode =
                           (sum of weighted deltas) * sigmoid_derivative

        Input Layer Node:
        No action taken.

        Args:
            expected: expected value
        """

        # Output Node
        if self.my_type == LayerType.OUTPUT:
            self.delta = (expected - self.value) * self.sigmoid_derivative(
                self.value)

        # Hidden Node
        sum_of_deltas = 0
        if self.my_type == LayerType.HIDDEN:
            for node in self.output_nodes:
                sum_of_deltas += (node.input_nodes[self] * node.delta)

            self.delta = sum_of_deltas * self.sigmoid_derivative(self.value)

    def update_weights(self):
        """
        This function uses this formula to calculate the new weight for each
        neurode in it's input_nodes dictionary:
        new weight =
            current weight + (
            input neurode value *
            our neurode's delta *
            learning rate)
        """
        new_weight = 0
        for index, node in enumerate(self.input_nodes):
            new_weight = self.input_nodes[node]
            new_weight += node.value * self.delta * self.learning_rate

            self.input_nodes[node] = new_weight

    def back_fire(self):
        """TODO Docs"""

        for node in self.input_nodes:
            if node.my_type is not LayerType.INPUT:
                node.receive_back_input(self)
