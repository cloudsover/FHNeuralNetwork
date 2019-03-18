"""TODO Docs"""

from InstructorSolutions.Network import FFBPNetwork
from InstructorSolutions import NNDataJson, NNData


class InteractiveMenu:
    """TODO Docs"""

    def __init__(self):
        """TODO Docs"""
        self.running = True
        self.data_loaded = False
        self.data = None
        self.train_percentage = 10
        self.network = FFBPNetwork(1, 1)

    def main_menu(self):
        """TODO Docs"""

        # TODO Load new Json
        # TODO Re-load Json
        # TODO Browse network layers
        # TODO Layer Type, Num Neurodes
        # TODO Add Layer after current
        # TODO Remove current layer
        # TODO Run network
        # TODO Quit
        pass

    def visualize_layer(self) -> str:
        """TODO Docs"""
        ret_string = ''
        layer_type, num_neurodes = self.network.layers.current.get_layer_info()
        ret_string += f'Current Layer Type:{layer_type}\n' \
            f'Neurodes in layer: {num_neurodes}\n'
        return ret_string

    def load_json(self, filename):
        """TODO Docs"""
        # TODO Make this work
        loaded = NNDataJson.decode_file(filename)
        return loaded

    def iterate_layers(self):
        """TODO Docs"""
        return self.network.iterate()

    def rev_iterate_layers(self):
        """TODO Docs"""
        return self.network.rev_iterate()

    def add_layer(self, num_neurodes):
        """TODO Docs"""
        return self.network.add_hidden_layer(num_neurodes)

    def remove_layer(self):
        """TODO Docs"""
        self.rev_iterate_layers()
        return self.network.remove_hidden_layer()

    def run_network(self, num_epochs, verbosity: int = 2,
                    order: NNData.ORDER = NNData.Order.SEQUENTIAL):
        """TODO Docs"""
        self.network.train(self.data, num_epochs, verbosity,
                           order)
        self.network.test(self.data, order)
