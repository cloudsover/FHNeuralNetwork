"""TODO Docs"""
import json

from Network import NNDataJson, NNData
from Network.FFBPNetwork import FFBPNetwork


class InteractiveMenu:
    """TODO Docs"""

    MAIN_MENU = f'Main Menu:\n 1) Load/Re-load Json\n 2)Browse Network ' \
        f'Layers\n 3)Run Network\n 4)Quit'

    LOAD_DATA = f'Please choose a data set:\n1)XOR Data\n 2)SIN Data\n 3)NEW'

    BROWSE = f'1)Move forward a layer\n2)Move backward a layer\n' \
        f'3)Add hidden layer\n 4)Remove hidden layer'

    def __init__(self):
        """TODO Docs"""
        self.running = True
        self.data_loaded = False
        self.data = None
        self.stored_data = {}
        self.train_percentage = 10
        self.network = FFBPNetwork(1, 1)
        self.data_stored = {"xor": None, "sin": None, "new": None}
        self.network.reset_cur()

    def main_menu(self):
        """TODO Docs"""

        while self.running:
            choice = None
            while choice is not type(int):
                choice = input(self.MAIN_MENU)
                if choice is not type(int):
                    print("Invalid Choice")
            if choice == 1:
                self.load_data()
            if choice == 2:
                self.browse_layers()
            if choice == 3:
                self.run()
            if choice == 4:
                self.running = False
                print("Goodbye")
        # TODO Browse network layers
        # TODO Layer Type, Num Neurodes
        # TODO Add Layer after current
        # TODO Remove current layer
        # TODO Run network
        # TODO Quit
        pass

    def load_data(self):
        """TODO Docs"""
        loading_data = True

        while loading_data:
            choice = None
            while choice is not type(int) and (choice < 4 and choice > 0):
                choice = input(self.LOAD_DATA)
            if choice == 1:
                self.load_json("xor")
                loading_data = False
            if choice == 2:
                self.load_json("sin")
                loading_data = False
            if choice == 3:
                self.load_json("new")
                loading_data = False

    def browse_layers(self):
        """TODO Docs"""
        browsing_layers = True

        while browsing_layers:
            self.visualize_layer()
            choice = None
            while choice is not type(int):
                choice = input(self.BROWSE)

    def visualize_layer(self) -> str:
        """TODO Docs"""
        ret_string = ''
        layer_type, num_neurodes = self.network.layers.current.get_layer_info()
        ret_string += f'Current Layer Type:{layer_type}\n'
        ret_string += f'Neurodes in layer: {num_neurodes}\n'
        return ret_string

    def load_json(self, filename):
        """TODO Docs"""
        # TODO Make this work
        self.data_loaded = json.loads(self.stored_data[filename],
                                      object_hook=NNDataJson.nn_data_decoder)

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

    def run(self):
        """TODO Docs"""
        pass

    def run_network(self, num_epochs, verbosity: int = 2,
                    order: NNData.Order = NNData.Order.SEQUENTIAL):
        """TODO Docs"""
        self.network.train(self.data, num_epochs, verbosity,
                           order)
        self.network.test(self.data, order)
