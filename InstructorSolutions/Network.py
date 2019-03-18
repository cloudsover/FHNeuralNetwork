import math

from InstructorSolutions import NNData
from InstructorSolutions.LayerList import LayerList


class FFBPNetwork:
    class EmptyLayerException(Exception):
        pass

    class EmptySetException(Exception):
        pass

    def __init__(self, num_inputs, num_outputs):
        self.layers = LayerList(num_inputs, num_outputs)
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs

    def add_hidden_layer(self, num_neurodes=5):
        if num_neurodes < 1:
            raise FFBPNetwork.EmptyLayerException
        self.layers.insert_hidden_layer(num_neurodes)

    def remove_hidden_layer(self):
        return self.layers.remove_hidden_layer()

    def iterate(self):
        return self.layers.iterate()

    def rev_iterate(self):
        return self.layers.rev_iterate()

    def reset_cur(self):
        return self.layers.reset_cur()

    def get_layer_info(self):
        return self.layers.current.get_layer_info()

    def train(self, data_set: NNData, epochs=1000, verbosity=2,
              order=NNData.Order.SEQUENTIAL):
        if data_set.get_number_samples(NNData.Set.TRAIN) == 0:
            raise FFBPNetwork.EmptySetException
        for epoch in range(0, epochs):
            data_set.prime_data(order=order)
            sum_error = 0
            while not data_set.empty_pool(NNData.Set.TRAIN):
                x, y = data_set.get_one_item(NNData.Set.TRAIN)
                for j, node in enumerate(self.layers.get_input_nodes()):
                    node.receive_input(None, x[j])
                produced = []
                for j, node in enumerate(self.layers.get_output_nodes()):
                    node.receive_back_input(None, y[j])
                    sum_error += (node.get_value() - y[
                        j]) ** 2 / self.num_outputs
                    produced.append(node.get_value())

                if epoch % 1000 == 0 and verbosity > 1:
                    print("Sample", x, "expected", y, "produced", produced)
            if epoch % 100 == 0 and verbosity > 0:
                print("Epoch", epoch, "RMSE = ", math.sqrt(
                    sum_error / data_set.get_number_samples(NNData.Set.TRAIN)))
        print("Final Epoch RMSE = ", math.sqrt(
            sum_error / data_set.get_number_samples(NNData.Set.TRAIN)))

    def test(self, data_set: NNData, order=NNData.Order.SEQUENTIAL):
        if data_set.get_number_samples(NNData.Set.TEST) == 0:
            raise FFBPNetwork.EmptySetException
        data_set.prime_data(order=order)
        sum_error = 0
        while not data_set.empty_pool(NNData.Set.TEST):
            x, y = data_set.get_one_item(NNData.Set.TEST)
            for j, node in enumerate(self.layers.get_input_nodes()):
                node.receive_input(None, x[j])
            produced = []
            for j, node in enumerate(self.layers.get_output_nodes()):
                sum_error += (node.get_value() - y[j]) ** 2 / self.num_outputs
                produced.append(node.get_value())

            print(x, ",", y, ",", produced)
        print("RMSE = ", math.sqrt(
            sum_error / data_set.get_number_samples(NNData.Set.TEST)))
