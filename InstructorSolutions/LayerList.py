from InstructorSolutions.DLLNode import DoublyLinkedList
from InstructorSolutions.Layer import Layer
from InstructorSolutions.MultiLinkNode import LayerType


class NodePositionError(Exception):
    pass


class LayerList(DoublyLinkedList):

    def __init__(self, num_inputs, num_outputs):
        super().__init__()
        input_layer = Layer(num_inputs, LayerType.INPUT)
        self.add_to_head(input_layer)
        self.reset_cur()
        output_layer = Layer(num_outputs, LayerType.OUTPUT)
        self.insert_after_cur(output_layer)

    def insert_after_cur(self, new_layer):

        if self.current.get_my_type() is LayerType.OUTPUT:
            raise NodePositionError

        # Add input nodes to our new layer
        for neurode in new_layer.get_my_neurodes():
            neurode.clear_and_add_input_nodes(self.current.get_my_neurodes())

        # Add our layer to the previous one
        for neurode in self.current.get_my_neurodes():
            neurode.clear_and_add_output_nodes(new_layer.get_my_neurodes())

        if new_layer.get_my_type() is LayerType.HIDDEN:

            # Add output nodes to our new layer
            for neurode in new_layer.get_my_neurodes():
                neurode.clear_and_add_output_nodes(
                    self.current.get_next().get_my_neurodes())

            # Add our layer to the next one
            for neurode in self.current.next.get_my_neurodes():
                neurode.clear_and_add_input_nodes(new_layer.get_my_neurodes())

        super().insert_after_cur(new_layer)

    def remove_after_cur(self):
        self.iterate()  # move on top of node to remove, to avoid ugly next.next references
        for neurode in self.current.get_next().get_my_neurodes():
            neurode.clear_and_add_input_nodes(
                self.current.get_prev().get_my_neurodes())

        for neurode in self.current.get_prev().get_my_neurodes():
            neurode.clear_and_add_output_nodes(
                self.current.get_next().get_my_neurodes())
        self.rev_iterate()  # move back so we can use the parent method
        super().remove_after_cur()

    def insert_hidden_layer(self, num_neurodes=5):
        if self.current == self.tail:
            raise NodePositionError
        hidden_layer = Layer(num_neurodes, LayerType.HIDDEN)
        self.insert_after_cur(hidden_layer)

    def remove_hidden_layer(self):
        if self.current.get_next().get_my_type() is not LayerType.HIDDEN:
            raise NodePositionError
        self.remove_after_cur()

    def get_input_nodes(self):
        return self.head.get_my_neurodes()
        # need to raise error if not set up

    def get_output_nodes(self):
        return self.tail.get_my_neurodes()
        # need ot raise error if not set up
