import copy

from Network.FFBPNeurode import FFBPNeurode
from Network.NNData import NNData
from Network.LayerList import LayerList
import numpy as np


class FFBPNetwork:
    """TODO Docs"""

    def __init__(self, num_inputs=1, num_outputs=1):
        """TODO Docs"""

        self.layers = LayerList(num_inputs, num_outputs)
        self.running_error = []
        self.csv = ''
        self.rmse_csv = 'epoch, rsme\n'

    def add_hidden_layer(self, num_neurodes: int = 5):
        """TODO Docs"""
        if num_neurodes < 1:
            raise FFBPNetwork.EmptyLayerException
        else:
            self.layers.insert_hidden_layer(num_neurodes)

    def train(self, data_set: NNData, epochs: int = 1000, verbosity=2):
        """TODO Docs"""

        if data_set is None:
            raise FFBPNetwork.EmptySetException

        else:
            print('TRAINING\n')
            size = data_set.get_number_samples(data_set.Set.TRAIN)
            for epoch in range(1, epochs + 1):
                epoch_data = copy.deepcopy(data_set)
                error = 0
                for data in range(size):

                    data = epoch_data.get_one_item(data_set.Set.TRAIN)
                    self.send_data_to_inputs(data[0])
                    error = self.calculate_error_for_example(data[1])
                    self.send_labels_to_outputs(data[1])
                    if verbosity > 1 and epoch > 1000:
                        print("\nEpoch:", epoch)
                        print(self.print_output_and_values(data[1]))
                    if verbosity > 0 and epoch % 100 == 0:
                        print("\nEpoch : ", epoch)
                        rmse = self.calculate_rmse(error, size)
                        print(self.print_rmse(rmse))

        print("\nFinal RMSE: ", epoch)
        self.rmse_csv += str(epochs) + ','
        rmse = self.calculate_rmse(error, size)
        print(self.print_rmse(rmse))

    def test(self, data_set: NNData):
        """TODO Docs"""
        if data_set is None:
            raise FFBPNetwork.EmptySetException
        else:
            print('\nTESTING:')
            self.csv = ''
            error = 0
            size = data_set.get_number_samples(data_set.Set.TEST)
            self.csv += 'Example, Predicted, Expected\n'
            datas = copy.deepcopy(data_set)
            for data in range(size):
                data = datas.get_one_item(data_set.Set.TEST)
                self.send_data_to_inputs(data[0])
                predicted = self.layers.output_layer.neurodes[0].get_value()
                error += self.calculate_error_for_example(data[1])
                self.csv += str(float(data[0])) + ','
                self.csv += str(predicted) + ','
                self.csv += str(float(data[1])) + '\n'

            print(self.csv)
            print("Final RMSE: ")
            rmse = self.calculate_rmse(error, size)
            self.rmse_csv += str(rmse) +'\n'
            print(self.print_rmse(rmse))

    # TODO Helper Functions ---------------------------------------------------

    # TODO Data Functions -----------------------------------------------------
    def send_data_to_inputs(self, example_data):
        """TODO Docs"""
        inputs: list[FFBPNeurode] = self.layers.input_layer.neurodes

        for node in inputs:
            node.receive_input(None, example_data)

    def send_labels_to_outputs(self, label_data):
        """TODO Docs"""
        outputs: list[FFBPNeurode] = self.layers.output_layer.neurodes

        for node in outputs:
            node.receive_back_input(None, label_data)

    # TODO Math Functions -----------------------------------------------------
    def calculate_error_for_example(self, expected):
        """TODO Docs"""
        outputs = self.layers.output_layer.neurodes
        error = 0
        for node in outputs:
            observed = node.get_value()
            error += observed - expected
        return error

    @staticmethod
    def calculate_rmse(error, size):
        """TODO Docs"""
        se = np.power(error, 2)
        mse = (1 / size) * se
        rmse = np.power(mse, 1 / 2)
        return rmse

    # TODO Printer Functions --------------------------------------------------
    def print_output_and_values(self, label_data):
        """TODO Docs"""
        outputs = self.layers.output_layer.neurodes

        ret_string = 'Observed Value: '
        for node in outputs:
            ret_string += '[' + str(node.get_value()) + ']'
        ret_string += '\nLabel Value: ' + str(label_data)
        return ret_string

    @staticmethod
    def print_rmse(rmse):
        """TODO Docs"""
        ret_string = 'RMSE: '
        ret_string += str(rmse)
        return ret_string

    def print_for_train_data(self, example_data, label_data):
        """TODO Docs"""
        pass

    class EmptyLayerException(Exception):
        """TODO Docs"""

    class EmptySetException(Exception):
        """TODO Docs"""


def main():
    network = FFBPNetwork(1, 1)
    network.add_hidden_layer(3)
    SINData = np.array(
        [[0, 0], [0.01, 0.00999983333416666], [0.02, 0.0199986666933331],
         [0.03, 0.0299955002024957], [0.04, 0.0399893341866342],
         [0.05, 0.0499791692706783], [0.06, 0.0599640064794446],
         [0.07, 0.0699428473375328], [0.08, 0.0799146939691727],
         [0.09, 0.089878549198011], [0.1, 0.0998334166468282],
         [0.11, 0.109778300837175], [0.12, 0.119712207288919],
         [0.13, 0.129634142619695], [0.14, 0.139543114644236],
         [0.15, 0.149438132473599], [0.16, 0.159318206614246],
         [0.17, 0.169182349066996], [0.18, 0.179029573425824],
         [0.19, 0.188858894976501], [0.2, 0.198669330795061],
         [0.21, 0.2084598998461], [0.22, 0.218229623080869],
         [0.23, 0.227977523535188], [0.24, 0.237702626427135],
         [0.25, 0.247403959254523], [0.26, 0.257080551892155],
         [0.27, 0.266731436688831], [0.28, 0.276355648564114],
         [0.29, 0.285952225104836], [0.3, 0.29552020666134],
         [0.31, 0.305058636443443], [0.32, 0.314566560616118],
         [0.33, 0.324043028394868], [0.34, 0.333487092140814],
         [0.35, 0.342897807455451], [0.36, 0.35227423327509],
         [0.37, 0.361615431964962], [0.38, 0.370920469412983],
         [0.39, 0.380188415123161], [0.4, 0.389418342308651],
         [0.41, 0.398609327984423], [0.42, 0.40776045305957],
         [0.43, 0.416870802429211], [0.44, 0.425939465066],
         [0.45, 0.43496553411123], [0.46, 0.44394810696552],
         [0.47, 0.452886285379068], [0.48, 0.461779175541483],
         [0.49, 0.470625888171158], [0.5, 0.479425538604203],
         [0.51, 0.488177246882907], [0.52, 0.496880137843737],
         [0.53, 0.505533341204847], [0.54, 0.514135991653113],
         [0.55, 0.522687228930659], [0.56, 0.531186197920883],
         [0.57, 0.539632048733969], [0.58, 0.548023936791874],
         [0.59, 0.556361022912784], [0.6, 0.564642473395035],
         [0.61, 0.572867460100481], [0.62, 0.581035160537305],
         [0.63, 0.58914475794227], [0.64, 0.597195441362392],
         [0.65, 0.60518640573604], [0.66, 0.613116851973434],
         [0.67, 0.62098598703656], [0.68, 0.628793024018469],
         [0.69, 0.636537182221968], [0.7, 0.644217687237691],
         [0.71, 0.651833771021537], [0.72, 0.659384671971473],
         [0.73, 0.666869635003698], [0.74, 0.674287911628145],
         [0.75, 0.681638760023334], [0.76, 0.688921445110551],
         [0.77, 0.696135238627357], [0.78, 0.70327941920041],
         [0.79, 0.710353272417608], [0.8, 0.717356090899523],
         [0.81, 0.724287174370143], [0.82, 0.731145829726896],
         [0.83, 0.737931371109963], [0.84, 0.744643119970859],
         [0.85, 0.751280405140293], [0.86, 0.757842562895277],
         [0.87, 0.764328937025505], [0.88, 0.770738878898969],
         [0.89, 0.777071747526824], [0.9, 0.783326909627483],
         [0.91, 0.78950373968995], [0.92, 0.795601620036366],
         [0.93, 0.801619940883777], [0.94, 0.807558100405114],
         [0.95, 0.813415504789374], [0.96, 0.819191568300998],
         [0.97, 0.82488571333845], [0.98, 0.83049737049197],
         [0.99, 0.836025978600521], [1, 0.841470984807897],
         [1.01, 0.846831844618015], [1.02, 0.852108021949363],
         [1.03, 0.857298989188603], [1.04, 0.862404227243338],
         [1.05, 0.867423225594017], [1.06, 0.872355482344986],
         [1.07, 0.877200504274682], [1.08, 0.881957806884948],
         [1.09, 0.886626914449487], [1.1, 0.891207360061435],
         [1.11, 0.895698685680048], [1.12, 0.900100442176505],
         [1.13, 0.904412189378826], [1.14, 0.908633496115883],
         [1.15, 0.912763940260521], [1.16, 0.916803108771767],
         [1.17, 0.920750597736136], [1.18, 0.92460601240802],
         [1.19, 0.928368967249167], [1.2, 0.932039085967226],
         [1.21, 0.935616001553386], [1.22, 0.939099356319068],
         [1.23, 0.942488801931697], [1.24, 0.945783999449539],
         [1.25, 0.948984619355586], [1.26, 0.952090341590516],
         [1.27, 0.955100855584692], [1.28, 0.958015860289225],
         [1.29, 0.960835064206073], [1.3, 0.963558185417193],
         [1.31, 0.966184951612734], [1.32, 0.968715100118265],
         [1.33, 0.971148377921045], [1.34, 0.973484541695319],
         [1.35, 0.975723357826659], [1.36, 0.977864602435316],
         [1.37, 0.979908061398614], [1.38, 0.98185353037236],
         [1.39, 0.983700814811277], [1.4, 0.98544972998846],
         [1.41, 0.98710010101385], [1.42, 0.98865176285172],
         [1.43, 0.990104560337178], [1.44, 0.991458348191686],
         [1.45, 0.992712991037588], [1.46, 0.993868363411645],
         [1.47, 0.994924349777581], [1.48, 0.99588084453764],
         [1.49, 0.996737752043143], [1.5, 0.997494986604054],
         [1.51, 0.998152472497548], [1.52, 0.998710143975583],
         [1.53, 0.999167945271476], [1.54, 0.999525830605479],
         [1.55, 0.999783764189357], [1.56, 0.999941720229966],
         [1.57, 0.999999682931835]])
    X = SINData[:, 0:1]
    Y = SINData[:, 1:2]
    max_epochs = 100000
    data = NNData(X, Y, 10)
    epoch = 100
    for i in range(max_epochs):
        network.train(data, epoch)
        network.test(data)

        file_name = 'epoch-' + str(epoch) + '.txt'
        with open(file_name, 'w', encoding='utf-8') as my_file:
            file = network.csv
            for line in file:
                my_file.write(line)

        epoch += 100
    with open('rmse-epoch.txt', 'w', encoding='utf-8') as my_file:
        file = network.rmse_csv
        for line in file:
            my_file.write(line)
    print('Fin')


main()
