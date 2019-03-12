# TODO Optimize imports, math
# TODO Take out getters and setters
from Network.Layer import Layer
from Network.LayerType import LayerType
from Network.DoublyLinkedList import DoublyLinkedList


class LayerList(DoublyLinkedList):
    """
    Controlling object which extends functionality of DoublyLinkedList.

    Handles adding and removing Layers of nodes (input, output, hidden).

    Attributes:
        input_layer: Layer object containing input FFBPNeurodes. This serves
        the same purpose as a 'head' pointer.

        output_layer: Layer object containing output FFBPNeurodes. This
        serves the same purpose as a 'tail' pointer.
    """

    def __init__(self, num_inputs: int, num_outputs: int):
        """
        Inits LayerList with all class attributes initialized.

        Args:
            num_inputs: number of input nodes in the input layer
            num_outputs: number of output nodes in the output layer
        """
        super().__init__()
        self.input_layer: Layer = Layer(num_inputs, LayerType.INPUT)
        self.output_layer = Layer(num_outputs, LayerType.OUTPUT)

        self.add_to_head(self.input_layer)
        self.reset_cur()
        self.reconnect_outputs(self.input_layer, self.output_layer)

        self.insert_after_cur(self.output_layer)

    def get_input_nodes(self) -> list:
        """
        Getter method which returns the list of input neurodes at the
        head of LayerList.

        Returns:
            list of input neurodes
        """
        return self.input_layer.get_my_neurodes()

    def get_output_nodes(self) -> list:
        """
        Getter method which returns a list of neurodes from the tail
        position of LayerList.

        Returns:
            list of output neurodes
        """

        return self.output_layer.get_my_neurodes()

    def insert_after_cur(self, new_layer):
        """
        Private Method
        Overridden method from base class. Resets connections between
        Neurodes after insertion.

        Args:
            new_layer: Layer to add into LayerList
        """
        from_layer = self.current
        if self.current is None:
            self.reset_cur()

        if new_layer.my_type is LayerType.OUTPUT:
            self.reconnect_nodes(from_layer, new_layer)
            super().insert_after_cur(new_layer)

        elif new_layer.my_type is LayerType.HIDDEN:
            self.reconnect_nodes(new_layer, from_layer)
            self.reconnect_nodes(self.current.get_next(), new_layer)
            super().insert_after_cur(new_layer)

        else:
            pass

    def remove_after_cur(self):
        """
        Private Method.
        Overridden method from base class. Resets connections between
        remaining neurodes, and clears connections from removed layer.

        """
        removed_nodes = self.current.get_next().get_my_neurodes()

        for node in removed_nodes:
            node.clear_outputs()
            node.clear_inputs()

        super().remove_after_cur()

        self.reconnect_inputs(self.current, self.current.get_next())

        self.reconnect_outputs(self.current.get_next(), self.current)

    def insert_hidden_layer(self, num_neurodes: int):
        """
        Method which inserts a hidden layer directly after the current
        position pointer.

        Args:
            num_neurodes: number of neurodes to be in the new hidden layer
        """
        if self.current is None:
            self.current = self.head

        if self.current is self.tail:
            raise NodePositionError
        else:
            self.insert_after_cur(Layer(num_neurodes, LayerType.HIDDEN))

    def remove_hidden_layer(self):
        """
        Method which removes a hidden layer directly after the current
        position pointer.
        """
        if self.current.get_next() is self.tail:
            raise NodePositionError
        else:
            self.remove_after_cur()

    def reconnect_nodes(self, input_layer, output_layer):
        """
        Helper method which reconnects input and output nodes between the
        given layers.

        Args:
            input_layer: layer which is designated as the input layer
            output_layer: layer which is designated as the output layer
        """
        self.reconnect_inputs(output_layer, input_layer)
        self.reconnect_outputs(input_layer, output_layer)

    @staticmethod
    def reconnect_inputs(from_layer: Layer, connect_to: Layer):
        """
        Static helper method which connects each node in the from_layer
        to input nodes in the connect_to

        Args:
            from_layer: layer to iterate through each node and connect to
            input nodes in connect_to
            connect_to: layer to connect each node in from_layer to
        """

        if from_layer.my_type is LayerType.INPUT:
            pass
        else:
            for node in from_layer.neurodes:
                node.clear_and_add_input_nodes(connect_to.neurodes)

    @staticmethod
    def reconnect_outputs(from_layer: Layer, connect_to: Layer):
        """
        Static helper method which connects each node in the from_layer
        to output nodes in the connect_to

        Args:
            from_layer: layer to iterate through each node and connect to
            output nodes in connect_to
            connect_to: layer to connect each node in from_layer to
        """
        if from_layer.my_type is LayerType.OUTPUT:
            pass
        else:
            for node in from_layer.neurodes:
                node.clear_and_add_output_nodes(connect_to.neurodes)


class NodePositionError(Exception):
    """Error that gets thrown if the pointer of LayerList is set to the
    head or tail."""
    pass


#
def main():
    # create a LayerList with two inputs and four outputs
    my_list = LayerList(2, 4)
    # get a list of the input and output nodes, and make sure we have the right number
    inputs = my_list.get_input_nodes()
    outputs = my_list.get_output_nodes()
    assert len(inputs) == 2
    assert len(outputs) == 4
    # check that each has the right number of connections
    for node in inputs:
        assert len(node.output_nodes) == 4
    for node in outputs:
        assert len(node.input_nodes) == 2
    # check that the connections go to the right place
    for node in inputs:
        out_set = set(node.output_nodes)
        check_set = set(outputs)
        assert out_set == check_set
    for node in outputs:
        in_set = set(node.input_nodes)
        check_set = set(inputs)
        assert in_set == check_set
    # add a couple layers and check that they arrived in the right order, and that iterate and rev_iterate work
    my_list.reset_cur()
    my_list.insert_hidden_layer(3)
    my_list.insert_hidden_layer(6)
    assert my_list.current.get_layer_info() == (LayerType.INPUT, 2)
    my_list.iterate()
    assert my_list.current.get_layer_info() == (LayerType.HIDDEN, 6)
    my_list.iterate()
    assert my_list.current.get_layer_info() == (LayerType.HIDDEN, 3)
    # save this layer to make sure it gets properly removed later
    save_layer_for_later = my_list.current
    my_list.iterate()
    assert my_list.current.get_layer_info() == (LayerType.OUTPUT, 4)
    my_list.rev_iterate()
    assert my_list.current.get_layer_info() == (LayerType.HIDDEN, 3)
    # check that information flows through all layers
    save_vals = []

    for node in outputs:
        save_vals.append(node.get_value())
    for node in inputs:
        node.receive_input(1)
    for i, node in enumerate(outputs):
        assert save_vals[i] != node.get_value()
    # check that information flows back as well
    save_vals = []
    for node in inputs[1].output_nodes:
        save_vals.append(node.get_delta())
    for node in outputs:
        node.receive_back_input(None, 1)
    for i, node in enumerate(inputs[1].output_nodes):
        assert save_vals[i] != node.get_delta()
    # try to remove an output layer
    try:
        my_list.remove_hidden_layer()
        assert False
    except NodePositionError:
        pass
    except:
        assert False
    # move and remove a hidden layer
    my_list.rev_iterate()
    my_list.remove_hidden_layer()
    # check the order of layers again
    my_list.reset_cur()
    assert my_list.current.get_layer_info() == (LayerType.INPUT, 2)
    my_list.iterate()
    assert my_list.current.get_layer_info() == (LayerType.HIDDEN, 6)
    my_list.iterate()
    assert my_list.current.get_layer_info() == (LayerType.OUTPUT, 4)
    my_list.rev_iterate()
    assert my_list.current.get_layer_info() == (LayerType.HIDDEN, 6)
    # save a value from the removed layer to make sure it doesn't get changed
    saved_val = save_layer_for_later.get_my_neurodes()[0].get_value()
    # check that information still flows through all layers
    save_vals = []
    for node in outputs:
        save_vals.append(node.get_value())
    for node in inputs:
        node.receive_input(input_value=1)
    for i, node in enumerate(outputs):
        assert save_vals[i] != node.get_value()
    # check that information still flows back as well
    save_vals = []
    for node in inputs[1].output_nodes:
        save_vals.append(node.get_delta())
    for node in outputs:
        node.receive_back_input(None, 1)
    for i, node in enumerate(inputs[1].output_nodes):
        assert save_vals[i] != node.get_delta()
    assert saved_val == save_layer_for_later.get_my_neurodes()[0].get_value()
    print("Done!")


main()
