"""Module which ties together the layers and nodes into a Neural Network."""

import numpy as np
import matplotlib.pyplot as plt
from Network.NNData import NNData
from Network.LayerList import LayerList


class FFBPNetwork:
    """
    Feed-Forward Back-Propagation neural network

    Attributes:
        layers: Layer list initialized with input and output layers in place
                with the number of nodes specified for each

    """

    def __init__(self, num_inputs=1, num_outputs=1):
        """Inits FFBPNetwork with all attributes initialized"""
        self.layers = LayerList(num_inputs, num_outputs)
        self._visualize_x = []
        self._visualize_y_nw = []
        self._visualize_y = []

    def add_hidden_layer(self, num_neurodes: int = 5):
        """
        Adds a hidden neurode layer into the layers LayerList with the
        given number of neurodes initialized.

        Args:
            num_neurodes (int): number of neurodes to initialize in the neural
            layer. Default value is 5.
        """
        if num_neurodes < 1:
            raise EmptyLayerException
        else:
            self.layers.insert_hidden_layer(num_neurodes)

    def train(self, data_set: NNData, epochs: int = 1000, verbosity=2,
              order=NNData.Order.RANDOM):
        """
        Runs the training data through the neural network for the given
        number of epochs.

        Args:
            data_set (NNData): Object containing the training data.
            epochs (int): number of epochs to train the data.
            verbosity: Level of print output desired
            order: Randomize, or keep data sequential.

        """
        if data_set.x is None:
            raise EmptySetException
        else:
            print("\nTraining:")

            for epoch in range(epochs):
                data_set.prime_data(NNData.Set.TRAIN, order)
                self.run_train_data(data_set, verbosity, epoch)

    def test(self, data_set: NNData, order=NNData.Order.RANDOM, one_hot=0):
        """
        This function runs the testing data through the neural network.

        Args:
            data_set (NNData): Object containing the testing data
            order: Order selection to randomize data or keep sequential
            one_hot: one hot encoding label data
        """

        if data_set.y is None:
            raise EmptySetException
        else:
            print("\nTesting:")
            data_set.prime_data(NNData.Set.TEST, order)
            rmse = self.run_test_data(data_set, one_hot)
            print("Final RMSE:", rmse)

    def iterate(self):
        """
        This function iterates the current pointer to the next
        layer.
        """
        self.layers.iterate()

    def rev_iterate(self):
        """This function reverse iterates the current pointer to the
        previous layer."""
        self.layers.rev_iterate()

    def reset_cur(self):
        """This function resets the current pointer to the input layer."""
        self.layers.reset_cur()

    def get_layer_info(self):
        """
        This function returns the current layer's info and returns type
        and number of neurons.

        Returns:
            Tuple of layer type and list of neurodes
        """
        self.layers.current.get_layer_info()

    # Data Functions ----------------------------------------------------------
    def send_data_to_inputs(self, data):
        """
        Helper function. Sends input data to the input nodes, iterating
        through each node and data value, if there is more than one value
        for the example data.

        Args:
            data (list): example data to send to the input layer nodes.
        """
        list_of_inputs = self.layers.get_input_nodes()

        for index, node in enumerate(list_of_inputs):
            node.receive_input(None, data[index])

    def send_data_to_outputs(self, data):
        """
        Helper function. Sends label data to the output nodes, iterating
        through each node and data value, if there is more than one value
        for the label data. The nodes then perform the back-propagation
        through the network with the expected values given from the label data.

        Args:
            data (list): example data to send to the output layer nodes.
        """
        list_of_outputs = self.layers.get_output_nodes()

        for index, node in enumerate(list_of_outputs):
            node.receive_back_input(None, data[index])

    def run_train_data(self, epoch_data: NNData, verbosity, epoch):
        """
        Helper function. Sends input data to the input layer, calculates
        the error from the output nodes against the expected values,
        and then sends the expected values to the output nodes to backprop
        through the network.

        Args:
            epoch_data (NNData): Object containing the data set.
            verbosity: how often to print epoch details
            epoch: current epoch

        Returns:
            The root mean squared error of the epoch. (float)
        """
        error = 0
        size = epoch_data.get_number_samples(NNData.Set.TRAIN)
        outputs = []
        labels = []
        for _ in range(size):
            single_data = epoch_data.get_one_item(NNData.Set.TRAIN)

            self.send_data_to_inputs(single_data[0])
            error += self.calculate_error(single_data[1])
            self.send_data_to_outputs(single_data[1])
            outputs.append(self.collect_outputs())
            labels.append(single_data[1])
        self.print_training_data(verbosity, epoch, outputs, labels,
                                 self.calculate_rmse(size, error))

    def run_test_data(self, epoch_data: NNData, one_hot=0) -> float:
        """
        Helper function. Runs testing pool example data through the input
        layer, and then compares the predicted values to the expected label
        values. Returns the root mean square error of the test run.

        Args:
            epoch_data (NNData): Object containing data set.
            one_hot: one hot encoding data

        Returns:
            rmse (float): Root mean squared error of the test run.
        """
        error = 0
        size = epoch_data.get_number_samples(NNData.Set.TEST)

        for _ in range(size):
            single_data = epoch_data.get_one_item(NNData.Set.TEST)
            self.send_data_to_inputs(single_data[0])
            self._visualize_x.append(single_data[0])
            self._visualize_y_nw.append(self.collect_outputs(one_hot))
            self._visualize_y.append(single_data[1])
            self.print_testing_data(single_data[0],
                                    self.collect_outputs(one_hot),
                                    single_data[1])
            error += self.calculate_error(single_data[1])
        return self.calculate_rmse(size, error)

    def collect_outputs(self, one_hot=0) -> list:
        """
        Helper function which gathers the values in the output layer and
        returns a list populated with their values.

        Returns:
            list of values from the output node layer
        """
        if one_hot == 1:
            return self.collect_one_hot()
        list_of_outputs = self.layers.get_output_nodes()
        output_data = []
        for node in list_of_outputs:
            output_data.append(node.value)
        return output_data

    def collect_one_hot(self) -> list:
        """TODO Docs"""
        list_of_outputs = self.layers.get_output_nodes()
        output_data = []
        for node in list_of_outputs:
            value = 0
            if node.value > .7:
                value = 1
            else:
                value = 0
            output_data.append(value)
        return output_data

    def _clear_vis(self):
        """Resets the two lists which hold the visualize data"""
        self._visualize_x = []
        self._visualize_y = []

    # Math Functions ----------------------------------------------------------
    def calculate_error(self, labels):
        """
        Helper function which calculates the squared error of each label
        against the predicted values from the output layer.

        Args:
            labels: expected label values to compare against observed
            values from output nodes.

        Returns:
            calculates the squared error of the output nodes

        """
        outputs = self.layers.get_output_nodes()
        size = outputs.__sizeof__()
        total_error = 0
        for index, node in enumerate(outputs):
            value = node.value
            error = value - labels[index]
            total_error += np.power(error, 2)
        return total_error / size

    @staticmethod
    def calculate_rmse(size: int, squared_error: float) -> float:
        """
        Static helper method which calculates the mean squared error given the
        size of the sample and the current squared error.

        Args:
            size (int): size of the sample data
            squared_error (float): current running squared error for data.

        Returns:
            Root mean squared error (float)
        """
        return np.sqrt(squared_error / size)

    # Print Functions ---------------------------------------------------------
    @staticmethod
    def print_training_data(verbosity, epoch, output: list,
                            label: list, rmse=0.0):
        """
        This function prints out observed values and expected values of the
        outputs every 1000 epochs, and prints out the epoch number and RMSE
        values every 100 epochs.

        Args:
            verbosity: if this value is less than 1, it will not print the
            label data. If this value is less than 0 it will print nothing
            epoch: current epoch
            output: list of output values
            label: list of label values
            rmse: root mean squared error

        Returns:
            Formatted output string of [output, label] data, and RMSE

        """

        if verbosity > 1 and epoch % 1000 == 0:
            ret_string = '['
            for i in range(len(output)):
                ret_string += str(output[i])
                ret_string += ', '
                ret_string += str(label[i])
                ret_string += ']\n'
            print(ret_string)
        if verbosity > 0 and epoch % 100 == 0:
            print("Epoch: ", epoch, "RMSE: ", rmse)

    @staticmethod
    def print_testing_data(input_values, output, label_data):
        """
        Printer function which prints the input values, observed output,
        and expected output values

        Args:
            input_values (list): input values
            output (list): output values, observed
            label_data (list): label values, expected

        Returns:
            prints out a formatted string
        """
        ret_string = ''

        ret_string += str(input_values)
        ret_string += ', '
        ret_string += str(output)
        ret_string += ', '
        ret_string += str(label_data)
        ret_string += ']'
        print(ret_string)

    # Plotting Functions ------------------------------------------------------

    def plot_output_comparison(self, scatter=0, plot=0):
        """
        Uses matplotlib to visualize the testing data

        """
        plt.ylim(top=2)
        plt.ylim(bottom=0)
        plt.xlim(left=0)
        plt.xlim(right=2)
        plt.xlim()
        if scatter == 1:
            plt.scatter(self._visualize_x, self._visualize_y, color='r')
            plt.scatter(self._visualize_x, self._visualize_y_nw, color='g')
        else:
            plt.plot(self._visualize_x, self._visualize_y, color='r')
            plt.plot(self._visualize_x, self._visualize_y_nw, color='g')
        plt.show()
        self._clear_vis()


class EmptyLayerException(Exception):
    """Layer is empty"""


class EmptySetException(Exception):
    """Data set is empty"""


def main():
    def run_iris():
        network = FFBPNetwork(4, 3)
        network.add_hidden_layer(6)

        Iris_X = [[5.1, 3.5, 1.4, 0.2], [4.9, 3, 1.4, 0.2],
                  [4.7, 3.2, 1.3, 0.2],
                  [4.6, 3.1, 1.5, 0.2],
                  [5, 3.6, 1.4, 0.2], [5.4, 3.9, 1.7, 0.4],
                  [4.6, 3.4, 1.4, 0.3],
                  [5, 3.4, 1.5, 0.2],
                  [4.4, 2.9, 1.4, 0.2], [4.9, 3.1, 1.5, 0.1],
                  [5.4, 3.7, 1.5, 0.2],
                  [4.8, 3.4, 1.6, 0.2],
                  [4.8, 3, 1.4, 0.1], [4.3, 3, 1.1, 0.1], [5.8, 4, 1.2, 0.2],
                  [5.7, 4.4, 1.5, 0.4],
                  [5.4, 3.9, 1.3, 0.4], [5.1, 3.5, 1.4, 0.3],
                  [5.7, 3.8, 1.7, 0.3],
                  [5.1, 3.8, 1.5, 0.3],
                  [5.4, 3.4, 1.7, 0.2], [5.1, 3.7, 1.5, 0.4],
                  [4.6, 3.6, 1, 0.2],
                  [5.1, 3.3, 1.7, 0.5],
                  [4.8, 3.4, 1.9, 0.2], [5, 3, 1.6, 0.2], [5, 3.4, 1.6, 0.4],
                  [5.2, 3.5, 1.5, 0.2],
                  [5.2, 3.4, 1.4, 0.2], [4.7, 3.2, 1.6, 0.2],
                  [4.8, 3.1, 1.6, 0.2],
                  [5.4, 3.4, 1.5, 0.4],
                  [5.2, 4.1, 1.5, 0.1], [5.5, 4.2, 1.4, 0.2],
                  [4.9, 3.1, 1.5, 0.1],
                  [5, 3.2, 1.2, 0.2],
                  [5.5, 3.5, 1.3, 0.2], [4.9, 3.1, 1.5, 0.1],
                  [4.4, 3, 1.3, 0.2],
                  [5.1, 3.4, 1.5, 0.2],
                  [5, 3.5, 1.3, 0.3], [4.5, 2.3, 1.3, 0.3],
                  [4.4, 3.2, 1.3, 0.2],
                  [5, 3.5, 1.6, 0.6],
                  [5.1, 3.8, 1.9, 0.4], [4.8, 3, 1.4, 0.3],
                  [5.1, 3.8, 1.6, 0.2],
                  [4.6, 3.2, 1.4, 0.2],
                  [5.3, 3.7, 1.5, 0.2], [5, 3.3, 1.4, 0.2], [7, 3.2, 4.7, 1.4],
                  [6.4, 3.2, 4.5, 1.5],
                  [6.9, 3.1, 4.9, 1.5], [5.5, 2.3, 4, 1.3],
                  [6.5, 2.8, 4.6, 1.5],
                  [5.7, 2.8, 4.5, 1.3],
                  [6.3, 3.3, 4.7, 1.6], [4.9, 2.4, 3.3, 1],
                  [6.6, 2.9, 4.6, 1.3],
                  [5.2, 2.7, 3.9, 1.4], [5, 2, 3.5, 1],
                  [5.9, 3, 4.2, 1.5], [6, 2.2, 4, 1], [6.1, 2.9, 4.7, 1.4],
                  [5.6, 2.9, 3.6, 1.3], [6.7, 3.1, 4.4, 1.4],
                  [5.6, 3, 4.5, 1.5], [5.8, 2.7, 4.1, 1], [6.2, 2.2, 4.5, 1.5],
                  [5.6, 2.5, 3.9, 1.1],
                  [5.9, 3.2, 4.8, 1.8], [6.1, 2.8, 4, 1.3],
                  [6.3, 2.5, 4.9, 1.5],
                  [6.1, 2.8, 4.7, 1.2],
                  [6.4, 2.9, 4.3, 1.3], [6.6, 3, 4.4, 1.4],
                  [6.8, 2.8, 4.8, 1.4],
                  [6.7, 3, 5, 1.7], [6, 2.9, 4.5, 1.5],
                  [5.7, 2.6, 3.5, 1], [5.5, 2.4, 3.8, 1.1], [5.5, 2.4, 3.7, 1],
                  [5.8, 2.7, 3.9, 1.2],
                  [6, 2.7, 5.1, 1.6], [5.4, 3, 4.5, 1.5], [6, 3.4, 4.5, 1.6],
                  [6.7, 3.1, 4.7, 1.5],
                  [6.3, 2.3, 4.4, 1.3], [5.6, 3, 4.1, 1.3], [5.5, 2.5, 4, 1.3],
                  [5.5, 2.6, 4.4, 1.2],
                  [6.1, 3, 4.6, 1.4], [5.8, 2.6, 4, 1.2], [5, 2.3, 3.3, 1],
                  [5.6, 2.7, 4.2, 1.3], [5.7, 3, 4.2, 1.2],
                  [5.7, 2.9, 4.2, 1.3], [6.2, 2.9, 4.3, 1.3],
                  [5.1, 2.5, 3, 1.1],
                  [5.7, 2.8, 4.1, 1.3],
                  [6.3, 3.3, 6, 2.5], [5.8, 2.7, 5.1, 1.9], [7.1, 3, 5.9, 2.1],
                  [6.3, 2.9, 5.6, 1.8],
                  [6.5, 3, 5.8, 2.2], [7.6, 3, 6.6, 2.1], [4.9, 2.5, 4.5, 1.7],
                  [7.3, 2.9, 6.3, 1.8],
                  [6.7, 2.5, 5.8, 1.8], [7.2, 3.6, 6.1, 2.5],
                  [6.5, 3.2, 5.1, 2],
                  [6.4, 2.7, 5.3, 1.9],
                  [6.8, 3, 5.5, 2.1], [5.7, 2.5, 5, 2], [5.8, 2.8, 5.1, 2.4],
                  [6.4, 3.2, 5.3, 2.3], [6.5, 3, 5.5, 1.8],
                  [7.7, 3.8, 6.7, 2.2], [7.7, 2.6, 6.9, 2.3], [6, 2.2, 5, 1.5],
                  [6.9, 3.2, 5.7, 2.3],
                  [5.6, 2.8, 4.9, 2], [7.7, 2.8, 6.7, 2], [6.3, 2.7, 4.9, 1.8],
                  [6.7, 3.3, 5.7, 2.1],
                  [7.2, 3.2, 6, 1.8], [6.2, 2.8, 4.8, 1.8], [6.1, 3, 4.9, 1.8],
                  [6.4, 2.8, 5.6, 2.1],
                  [7.2, 3, 5.8, 1.6], [7.4, 2.8, 6.1, 1.9], [7.9, 3.8, 6.4, 2],
                  [6.4, 2.8, 5.6, 2.2],
                  [6.3, 2.8, 5.1, 1.5], [6.1, 2.6, 5.6, 1.4],
                  [7.7, 3, 6.1, 2.3],
                  [6.3, 3.4, 5.6, 2.4],
                  [6.4, 3.1, 5.5, 1.8], [6, 3, 4.8, 1.8], [6.9, 3.1, 5.4, 2.1],
                  [6.7, 3.1, 5.6, 2.4],
                  [6.9, 3.1, 5.1, 2.3], [5.8, 2.7, 5.1, 1.9],
                  [6.8, 3.2, 5.9, 2.3],
                  [6.7, 3.3, 5.7, 2.5],
                  [6.7, 3, 5.2, 2.3], [6.3, 2.5, 5, 1.9], [6.5, 3, 5.2, 2],
                  [6.2, 3.4, 5.4, 2.3], [5.9, 3, 5.1, 1.8]]
        Iris_Y = [[1, 0, 0, ], [1, 0, 0, ], [1, 0, 0, ], [1, 0, 0, ],
                  [1, 0, 0, ],
                  [1, 0, 0, ], [1, 0, 0, ],
                  [1, 0, 0, ], [1, 0, 0, ], [1, 0, 0, ], [1, 0, 0, ],
                  [1, 0, 0, ],
                  [1, 0, 0, ], [1, 0, 0, ],
                  [1, 0, 0, ], [1, 0, 0, ], [1, 0, 0, ], [1, 0, 0, ],
                  [1, 0, 0, ],
                  [1, 0, 0, ], [1, 0, 0, ],
                  [1, 0, 0, ], [1, 0, 0, ], [1, 0, 0, ], [1, 0, 0, ],
                  [1, 0, 0, ],
                  [1, 0, 0, ], [1, 0, 0, ],
                  [1, 0, 0, ], [1, 0, 0, ], [1, 0, 0, ], [1, 0, 0, ],
                  [1, 0, 0, ],
                  [1, 0, 0, ], [1, 0, 0, ],
                  [1, 0, 0, ], [1, 0, 0, ], [1, 0, 0, ], [1, 0, 0, ],
                  [1, 0, 0, ],
                  [1, 0, 0, ], [1, 0, 0, ],
                  [1, 0, 0, ], [1, 0, 0, ], [1, 0, 0, ], [1, 0, 0, ],
                  [1, 0, 0, ],
                  [1, 0, 0, ], [1, 0, 0, ],
                  [1, 0, 0, ], [0, 1, 0, ], [0, 1, 0, ], [0, 1, 0, ],
                  [0, 1, 0, ],
                  [0, 1, 0, ], [0, 1, 0, ],
                  [0, 1, 0, ], [0, 1, 0, ], [0, 1, 0, ], [0, 1, 0, ],
                  [0, 1, 0, ],
                  [0, 1, 0, ], [0, 1, 0, ],
                  [0, 1, 0, ], [0, 1, 0, ], [0, 1, 0, ], [0, 1, 0, ],
                  [0, 1, 0, ],
                  [0, 1, 0, ], [0, 1, 0, ],
                  [0, 1, 0, ], [0, 1, 0, ], [0, 1, 0, ], [0, 1, 0, ],
                  [0, 1, 0, ],
                  [0, 1, 0, ], [0, 1, 0, ],
                  [0, 1, 0, ], [0, 1, 0, ], [0, 1, 0, ], [0, 1, 0, ],
                  [0, 1, 0, ],
                  [0, 1, 0, ], [0, 1, 0, ],
                  [0, 1, 0, ], [0, 1, 0, ], [0, 1, 0, ], [0, 1, 0, ],
                  [0, 1, 0, ],
                  [0, 1, 0, ], [0, 1, 0, ],
                  [0, 1, 0, ], [0, 1, 0, ], [0, 1, 0, ], [0, 1, 0, ],
                  [0, 1, 0, ],
                  [0, 1, 0, ], [0, 1, 0, ],
                  [0, 1, 0, ], [0, 1, 0, ], [0, 0, 1, ], [0, 0, 1, ],
                  [0, 0, 1, ],
                  [0, 0, 1, ], [0, 0, 1, ],
                  [0, 0, 1, ], [0, 0, 1, ], [0, 0, 1, ], [0, 0, 1, ],
                  [0, 0, 1, ],
                  [0, 0, 1, ], [0, 0, 1, ],
                  [0, 0, 1, ], [0, 0, 1, ], [0, 0, 1, ], [0, 0, 1, ],
                  [0, 0, 1, ],
                  [0, 0, 1, ], [0, 0, 1, ],
                  [0, 0, 1, ], [0, 0, 1, ], [0, 0, 1, ], [0, 0, 1, ],
                  [0, 0, 1, ],
                  [0, 0, 1, ], [0, 0, 1, ],
                  [0, 0, 1, ], [0, 0, 1, ], [0, 0, 1, ], [0, 0, 1, ],
                  [0, 0, 1, ],
                  [0, 0, 1, ], [0, 0, 1, ],
                  [0, 0, 1, ], [0, 0, 1, ], [0, 0, 1, ], [0, 0, 1, ],
                  [0, 0, 1, ],
                  [0, 0, 1, ], [0, 0, 1, ],
                  [0, 0, 1, ], [0, 0, 1, ], [0, 0, 1, ], [0, 0, 1, ],
                  [0, 0, 1, ],
                  [0, 0, 1, ], [0, 0, 1, ],
                  [0, 0, 1, ], [0, 0, 1, ], [0, 0, 1, ]]
        data = NNData(Iris_X, Iris_Y, 45)
        network.train(data, 1001, verbosity=0)
        network.test(data, one_hot=1)

    def run_sin():
        network = FFBPNetwork(1, 1)
        network.add_hidden_layer(25)
        sin_X = [[0], [0.01], [0.02], [0.03], [0.04], [0.05], [0.06], [0.07],
                 [0.08], [0.09], [0.1], [0.11], [0.12],
                 [0.13], [0.14], [0.15], [0.16], [0.17], [0.18], [0.19], [0.2],
                 [0.21], [0.22], [0.23], [0.24], [0.25],
                 [0.26], [0.27], [0.28], [0.29], [0.3], [0.31], [0.32], [0.33],
                 [0.34], [0.35], [0.36], [0.37], [0.38],
                 [0.39], [0.4], [0.41], [0.42], [0.43], [0.44], [0.45], [0.46],
                 [0.47], [0.48], [0.49], [0.5], [0.51],
                 [0.52], [0.53], [0.54], [0.55], [0.56], [0.57], [0.58],
                 [0.59],
                 [0.6], [0.61], [0.62], [0.63], [0.64],
                 [0.65], [0.66], [0.67], [0.68], [0.69], [0.7], [0.71], [0.72],
                 [0.73], [0.74], [0.75], [0.76], [0.77],
                 [0.78], [0.79], [0.8], [0.81], [0.82], [0.83], [0.84], [0.85],
                 [0.86], [0.87], [0.88], [0.89], [0.9],
                 [0.91], [0.92], [0.93], [0.94], [0.95], [0.96], [0.97],
                 [0.98],
                 [0.99], [1], [1.01], [1.02], [1.03],
                 [1.04], [1.05], [1.06], [1.07], [1.08], [1.09], [1.1], [1.11],
                 [1.12], [1.13], [1.14], [1.15], [1.16],
                 [1.17], [1.18], [1.19], [1.2], [1.21], [1.22], [1.23], [1.24],
                 [1.25], [1.26], [1.27], [1.28], [1.29],
                 [1.3], [1.31], [1.32], [1.33], [1.34], [1.35], [1.36], [1.37],
                 [1.38], [1.39], [1.4], [1.41], [1.42],
                 [1.43], [1.44], [1.45], [1.46], [1.47], [1.48], [1.49], [1.5],
                 [1.51], [1.52], [1.53], [1.54], [1.55],
                 [1.56], [1.57]]
        sin_Y = [[0], [0.00999983333416666], [0.0199986666933331],
                 [0.0299955002024957], [0.0399893341866342],
                 [0.0499791692706783], [0.0599640064794446],
                 [0.0699428473375328],
                 [0.0799146939691727],
                 [0.089878549198011], [0.0998334166468282],
                 [0.109778300837175],
                 [0.119712207288919],
                 [0.129634142619695], [0.139543114644236], [0.149438132473599],
                 [0.159318206614246],
                 [0.169182349066996], [0.179029573425824], [0.188858894976501],
                 [0.198669330795061], [0.2084598998461],
                 [0.218229623080869], [0.227977523535188], [0.237702626427135],
                 [0.247403959254523],
                 [0.257080551892155], [0.266731436688831], [0.276355648564114],
                 [0.285952225104836], [0.29552020666134],
                 [0.305058636443443], [0.314566560616118], [0.324043028394868],
                 [0.333487092140814],
                 [0.342897807455451], [0.35227423327509], [0.361615431964962],
                 [0.370920469412983], [0.380188415123161],
                 [0.389418342308651], [0.398609327984423], [0.40776045305957],
                 [0.416870802429211], [0.425939465066],
                 [0.43496553411123], [0.44394810696552], [0.452886285379068],
                 [0.461779175541483], [0.470625888171158],
                 [0.479425538604203], [0.488177246882907], [0.496880137843737],
                 [0.505533341204847],
                 [0.514135991653113], [0.522687228930659], [0.531186197920883],
                 [0.539632048733969],
                 [0.548023936791874], [0.556361022912784], [0.564642473395035],
                 [0.572867460100481],
                 [0.581035160537305], [0.58914475794227], [0.597195441362392],
                 [0.60518640573604], [0.613116851973434],
                 [0.62098598703656], [0.628793024018469], [0.636537182221968],
                 [0.644217687237691], [0.651833771021537],
                 [0.659384671971473], [0.666869635003698], [0.674287911628145],
                 [0.681638760023334],
                 [0.688921445110551], [0.696135238627357], [0.70327941920041],
                 [0.710353272417608], [0.717356090899523],
                 [0.724287174370143], [0.731145829726896], [0.737931371109963],
                 [0.744643119970859],
                 [0.751280405140293], [0.757842562895277], [0.764328937025505],
                 [0.770738878898969],
                 [0.777071747526824], [0.783326909627483], [0.78950373968995],
                 [0.795601620036366], [0.801619940883777],
                 [0.807558100405114], [0.813415504789374], [0.819191568300998],
                 [0.82488571333845], [0.83049737049197],
                 [0.836025978600521], [0.841470984807897], [0.846831844618015],
                 [0.852108021949363],
                 [0.857298989188603], [0.862404227243338], [0.867423225594017],
                 [0.872355482344986],
                 [0.877200504274682], [0.881957806884948], [0.886626914449487],
                 [0.891207360061435],
                 [0.895698685680048], [0.900100442176505], [0.904412189378826],
                 [0.908633496115883],
                 [0.912763940260521], [0.916803108771767], [0.920750597736136],
                 [0.92460601240802], [0.928368967249167],
                 [0.932039085967226], [0.935616001553386], [0.939099356319068],
                 [0.942488801931697],
                 [0.945783999449539], [0.948984619355586], [0.952090341590516],
                 [0.955100855584692],
                 [0.958015860289225], [0.960835064206073], [0.963558185417193],
                 [0.966184951612734],
                 [0.968715100118265], [0.971148377921045], [0.973484541695319],
                 [0.975723357826659],
                 [0.977864602435316], [0.979908061398614], [0.98185353037236],
                 [0.983700814811277], [0.98544972998846],
                 [0.98710010101385], [0.98865176285172], [0.990104560337178],
                 [0.991458348191686], [0.992712991037588],
                 [0.993868363411645], [0.994924349777581], [0.99588084453764],
                 [0.996737752043143], [0.997494986604054],
                 [0.998152472497548], [0.998710143975583], [0.999167945271476],
                 [0.999525830605479],
                 [0.999783764189357], [0.999941720229966], [0.999999682931835]]
        data = NNData(sin_X, sin_Y, 45)
        network.train(data, 1, verbosity=1)
        network.test(data)
        network.plot_output_comparison()

    def run_XOR():
        network = FFBPNetwork(2, 1)
        network.add_hidden_layer(3)
        XORx = [[0, 0], [1, 0], [0, 1], [1, 1]]
        XORy = [[0], [1], [1], [0]]
        data = NNData(XORx, XORy, 100)
        network.train(data, 1001)
        network.test(data, one_hot=1)

    def run_tests():
        network = FFBPNetwork(1, 1)
        network.add_hidden_layer(3)
        network.add_hidden_layer(4)
        network.layers.reset_cur()
        while True:
            print(network.layers.current.get_layer_info())
            if not network.layers.iterate():
                break
        network.layers.reset_cur()
        network.layers.iterate()
        network.layers.remove_hidden_layer()
        network.layers.reset_cur()
        while True:
            print(network.layers.current.get_layer_info())
            if not network.layers.iterate():
                break

    # run_tests()
    # run_iris()
    run_sin()
    # run_XOR()


if __name__ == "__main__":
    main()
