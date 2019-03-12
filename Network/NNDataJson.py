"""This module encodes and decodes NNData objects to and from json objects"""
import json
from collections import deque
from Network.NNData import NNData
from Network.FFBPNetwork import FFBPNetwork


def read_file(data_file: NNData):
    """
    This helper function takes in a NNData object and outputs the class
    attributes to translate in the json encoder

    Args:
        data_file: NNData object to read
    Returns:
        x_data (list) : x example data
        y_data (list) : y label data
        train_percentage (int) : percentage of train data
        train_pool (deque): train pool data
        test_pool (deque): testing pool data
        test_indices (list): test indices pointers
        train_indices (list): train indices pointers
    """
    x_data = data_file.x
    y_data = data_file.y
    train_percentage = data_file.train_percentage
    test_pool = data_file.test_pool
    train_pool = data_file.train_pool
    test_indices = data_file.test_indices
    train_indices = data_file.train_indices

    return x_data, y_data, train_percentage, list(train_pool), \
           list(test_pool), test_indices, train_indices


def encode_file(file_name: NNData) -> json:
    """
    Takes in a NNData object and outputs an encoded JSON file

    Args:
        file_name: NNData object to encode

    Returns:
        encoded json file
    """
    x_data, y_data, percentage, train, test, test_index, train_index = \
        read_file(file_name)

    data = {"__NNData__": {"train_percentage": percentage,
                           "x": x_data,
                           "y": y_data,
                           "train_indices": train_index,
                           "test_indices": test_index,
                           "train_pool": {'__deque__': train},
                           "test_pool": {'__deque__': test}}}
    return json.dumps(data)


def decode_file(file: json) -> NNData:
    """
    Takes in a json file and outputs a NNData object

    Args:
        file: json object to decode

    Returns:
        NNData object with all attributes initialized
    """
    dct = json.loads(file)
    data = dct['__NNData__']
    new_data = NNData(data['x'], data['y'], data['train_percentage'])
    new_data.train_indices = data['train_indices']
    new_data.test_indices = data['test_indices']

    test_pool = data['test_pool']
    train_pool = data['train_pool']
    new_data.test_pool = deque(test_pool['__deque__'])
    new_data.train_pool = deque(train_pool['__deque__'])
    new_data.train_data = (new_data.train_indices, new_data.train_pool)
    new_data.test_data = (new_data.test_indices, new_data.test_pool)

    return new_data


def main():
    """Main Unit test for module"""

    xor_x = [[0, 0], [1, 0], [0, 1], [1, 1]]
    xor_y = [[0], [1], [1], [0]]
    xor_data = NNData(xor_x, xor_y, 90)

    xor_data_encoded = encode_file(xor_data)
    xor_data_decoded = decode_file(xor_data_encoded)

    network = FFBPNetwork(2, 1)
    network.add_hidden_layer(3)
    network.train(xor_data_decoded, 1001)
    network.test(xor_data_decoded, one_hot=1)

    sin_json = """{"__NNData__": {"train_percentage": 10,
                                  "x": [[0.0], [0.01], [0.02], [0.03], [0.04],
                                        [0.05], [0.06], [0.07], [0.08], [0.09],
                                        [0.1], [0.11], [0.12], [0.13], [0.14],
                                        [0.15], [0.16], [0.17], [0.18], [0.19],
                                        [0.2], [0.21], [0.22], [0.23], [0.24],
                                        [0.25], [0.26], [0.27], [0.28], [0.29],
                                        [0.3], [0.31], [0.32], [0.33], [0.34],
                                        [0.35], [0.36], [0.37], [0.38], [0.39],
                                        [0.4], [0.41], [0.42], [0.43], [0.44],
                                        [0.45], [0.46], [0.47], [0.48], [0.49],
                                        [0.5], [0.51], [0.52], [0.53], [0.54],
                                        [0.55], [0.56], [0.57], [0.58], [0.59],
                                        [0.6], [0.61], [0.62], [0.63], [0.64],
                                        [0.65], [0.66], [0.67], [0.68], [0.69],
                                        [0.7], [0.71], [0.72], [0.73], [0.74],
                                        [0.75], [0.76], [0.77], [0.78], [0.79],
                                        [0.8], [0.81], [0.82], [0.83], [0.84],
                                        [0.85], [0.86], [0.87], [0.88], [0.89],
                                        [0.9], [0.91], [0.92], [0.93], [0.94],
                                        [0.95], [0.96], [0.97], [0.98], [0.99],
                                        [1.0], [1.01], [1.02], [1.03], [1.04],
                                        [1.05], [1.06], [1.07], [1.08], [1.09],
                                        [1.1], [1.11], [1.12], [1.13], [1.14],
                                        [1.15], [1.16], [1.17], [1.18], [1.19],
                                        [1.2], [1.21], [1.22], [1.23], [1.24],
                                        [1.25], [1.26], [1.27], [1.28], [1.29],
                                        [1.3], [1.31], [1.32], [1.33], [1.34],
                                        [1.35], [1.36], [1.37], [1.38], [1.39],
                                        [1.4], [1.41], [1.42], [1.43], [1.44],
                                        [1.45], [1.46], [1.47], [1.48], [1.49],
                                        [1.5], [1.51], [1.52], [1.53], [1.54],
                                        [1.55], [1.56], [1.57], [1.58], [1.59],
                                        [1.6], [1.61], [1.62], [1.63], [1.64],
                                        [1.65], [1.66], [1.67], [1.68], [1.69],
                                        [1.7], [1.71], [1.72], [1.73], [1.74],
                                        [1.75], [1.76], [1.77], [1.78], [1.79],
                                        [1.8], [1.81], [1.82], [1.83], [1.84],
                                        [1.85], [1.86], [1.87], [1.88], [1.89],
                                        [1.9], [1.91], [1.92], [1.93], [1.94],
                                        [1.95], [1.96], [1.97], [1.98], [1.99],
                                        [2.0], [2.01], [2.02], [2.03], [2.04],
                                        [2.05], [2.06], [2.07], [2.08], [2.09],
                                        [2.1], [2.11], [2.12], [2.13], [2.14],
                                        [2.15], [2.16], [2.17], [2.18], [2.19],
                                        [2.2], [2.21], [2.22], [2.23], [2.24],
                                        [2.25], [2.26], [2.27], [2.28], [2.29],
                                        [2.3], [2.31], [2.32], [2.33], [2.34],
                                        [2.35], [2.36], [2.37], [2.38], [2.39],
                                        [2.4], [2.41], [2.42], [2.43], [2.44],
                                        [2.45], [2.46], [2.47], [2.48], [2.49],
                                        [2.5], [2.51], [2.52], [2.53], [2.54],
                                        [2.55], [2.56], [2.57], [2.58], [2.59],
                                        [2.6], [2.61], [2.62], [2.63], [2.64],
                                        [2.65], [2.66], [2.67], [2.68], [2.69],
                                        [2.7], [2.71], [2.72], [2.73], [2.74],
                                        [2.75], [2.76], [2.77], [2.78], [2.79],
                                        [2.8], [2.81], [2.82], [2.83], [2.84],
                                        [2.85], [2.86], [2.87], [2.88], [2.89],
                                        [2.9], [2.91], [2.92], [2.93], [2.94],
                                        [2.95], [2.96], [2.97], [2.98], [2.99],
                                        [3.0], [3.01], [3.02], [3.03], [3.04],
                                        [3.05], [3.06], [3.07], [3.08], [3.09],
                                        [3.1], [3.11], [3.12], [3.13], [3.14]],
                                  "y": [[0.0], [0.00999983333416666],
                                        [0.0199986666933331],
                                        [0.0299955002024957],
                                        [0.0399893341866342],
                                        [0.0499791692706783],
                                        [0.0599640064794446],
                                        [0.0699428473375328],
                                        [0.0799146939691727],
                                        [0.089878549198011],
                                        [0.0998334166468282],
                                        [0.109778300837175],
                                        [0.119712207288919],
                                        [0.129634142619695],
                                        [0.139543114644236],
                                        [0.149438132473599],
                                        [0.159318206614246],
                                        [0.169182349066996],
                                        [0.179029573425824],
                                        [0.188858894976501],
                                        [0.198669330795061], [0.2084598998461],
                                        [0.218229623080869],
                                        [0.227977523535188],
                                        [0.237702626427135],
                                        [0.247403959254523],
                                        [0.257080551892155],
                                        [0.266731436688831],
                                        [0.276355648564114],
                                        [0.285952225104836],
                                        [0.29552020666134],
                                        [0.305058636443443],
                                        [0.314566560616118],
                                        [0.324043028394868],
                                        [0.333487092140814],
                                        [0.342897807455451],
                                        [0.35227423327509],
                                        [0.361615431964962],
                                        [0.370920469412983],
                                        [0.380188415123161],
                                        [0.389418342308651],
                                        [0.398609327984423],
                                        [0.40776045305957],
                                        [0.416870802429211], [0.425939465066],
                                        [0.43496553411123], [0.44394810696552],
                                        [0.452886285379068],
                                        [0.461779175541483],
                                        [0.470625888171158],
                                        [0.479425538604203],
                                        [0.488177246882907],
                                        [0.496880137843737],
                                        [0.505533341204847],
                                        [0.514135991653113],
                                        [0.522687228930659],
                                        [0.531186197920883],
                                        [0.539632048733969],
                                        [0.548023936791874],
                                        [0.556361022912784],
                                        [0.564642473395035],
                                        [0.572867460100481],
                                        [0.581035160537305],
                                        [0.58914475794227],
                                        [0.597195441362392],
                                        [0.60518640573604],
                                        [0.613116851973434],
                                        [0.62098598703656],
                                        [0.628793024018469],
                                        [0.636537182221968],
                                        [0.644217687237691],
                                        [0.651833771021537],
                                        [0.659384671971473],
                                        [0.666869635003698],
                                        [0.674287911628145],
                                        [0.681638760023334],
                                        [0.688921445110551],
                                        [0.696135238627357],
                                        [0.70327941920041],
                                        [0.710353272417608],
                                        [0.717356090899523],
                                        [0.724287174370143],
                                        [0.731145829726896],
                                        [0.737931371109963],
                                        [0.744643119970859],
                                        [0.751280405140293],
                                        [0.757842562895277],
                                        [0.764328937025505],
                                        [0.770738878898969],
                                        [0.777071747526824],
                                        [0.783326909627483],
                                        [0.78950373968995],
                                        [0.795601620036366],
                                        [0.801619940883777],
                                        [0.807558100405114],
                                        [0.813415504789374],
                                        [0.819191568300998],
                                        [0.82488571333845], [0.83049737049197],
                                        [0.836025978600521],
                                        [0.841470984807897],
                                        [0.846831844618015],
                                        [0.852108021949363],
                                        [0.857298989188603],
                                        [0.862404227243338],
                                        [0.867423225594017],
                                        [0.872355482344986],
                                        [0.877200504274682],
                                        [0.881957806884948],
                                        [0.886626914449487],
                                        [0.891207360061435],
                                        [0.895698685680048],
                                        [0.900100442176505],
                                        [0.904412189378826],
                                        [0.908633496115883],
                                        [0.912763940260521],
                                        [0.916803108771767],
                                        [0.920750597736136],
                                        [0.92460601240802],
                                        [0.928368967249167],
                                        [0.932039085967226],
                                        [0.935616001553386],
                                        [0.939099356319068],
                                        [0.942488801931697],
                                        [0.945783999449539],
                                        [0.948984619355586],
                                        [0.952090341590516],
                                        [0.955100855584692],
                                        [0.958015860289225],
                                        [0.960835064206073],
                                        [0.963558185417193],
                                        [0.966184951612734],
                                        [0.968715100118265],
                                        [0.971148377921045],
                                        [0.973484541695319],
                                        [0.975723357826659],
                                        [0.977864602435316],
                                        [0.979908061398614],
                                        [0.98185353037236],
                                        [0.983700814811277],
                                        [0.98544972998846], [0.98710010101385],
                                        [0.98865176285172],
                                        [0.990104560337178],
                                        [0.991458348191686],
                                        [0.992712991037588],
                                        [0.993868363411645],
                                        [0.994924349777581],
                                        [0.99588084453764],
                                        [0.996737752043143],
                                        [0.997494986604054],
                                        [0.998152472497548],
                                        [0.998710143975583],
                                        [0.999167945271476],
                                        [0.999525830605479],
                                        [0.999783764189357],
                                        [0.999941720229966],
                                        [0.999999682931835],
                                        [0.99995764649874],
                                        [0.999815615134291],
                                        [0.999573603041505],
                                        [0.999231634421391],
                                        [0.998789743470524],
                                        [0.998247974377632],
                                        [0.997606381319174],
                                        [0.996865028453919],
                                        [0.996023989916537],
                                        [0.99508334981018],
                                        [0.994043202198076],
                                        [0.992903651094118],
                                        [0.991664810452469],
                                        [0.990326804156158],
                                        [0.988889766004701],
                                        [0.987353839700716],
                                        [0.985719178835553],
                                        [0.983985946873937],
                                        [0.982154317137618],
                                        [0.980224472788045],
                                        [0.978196606808045],
                                        [0.976070921982524],
                                        [0.973847630878195],
                                        [0.971526955822315],
                                        [0.969109128880456],
                                        [0.966594391833298],
                                        [0.963982996152448], [0.9612752029753],
                                        [0.958471283078914],
                                        [0.955571516852944],
                                        [0.952576194271595],
                                        [0.94948561486463],
                                        [0.946300087687414],
                                        [0.943019931290011],
                                        [0.939645473685325],
                                        [0.936177052316306], [0.9326150140222],
                                        [0.928959715003869],
                                        [0.925211520788168],
                                        [0.921370806191395],
                                        [0.91743795528181],
                                        [0.913413361341225],
                                        [0.909297426825682],
                                        [0.905090563325201],
                                        [0.900793191522627],
                                        [0.89640574115156], [0.89192865095338],
                                        [0.887362368633375],
                                        [0.882707350815974],
                                        [0.877964062999078],
                                        [0.873132979507516],
                                        [0.868214583445613],
                                        [0.863209366648874],
                                        [0.858117829634809],
                                        [0.852940481552876],
                                        [0.84767784013357],
                                        [0.842330431636646],
                                        [0.836898790798498],
                                        [0.831383460778683],
                                        [0.825784993105608],
                                        [0.820103947621374],
                                        [0.814340892425796],
                                        [0.80849640381959],
                                        [0.802571066246747],
                                        [0.796565472236087],
                                        [0.790480222342005],
                                        [0.78431592508442],
                                        [0.778073196887921],
                                        [0.771752662020126],
                                        [0.765354952529254],
                                        [0.758880708180922],
                                        [0.752330576394171],
                                        [0.74570521217672],
                                        [0.739005278059471],
                                        [0.732231444030251],
                                        [0.72538438746682],
                                        [0.718464793069126],
                                        [0.711473352790844],
                                        [0.704410765770176],
                                        [0.697277738259938],
                                        [0.690074983556936],
                                        [0.68280322193064],
                                        [0.675463180551151],
                                        [0.668055593416491],
                                        [0.660581201279201],
                                        [0.653040751572265],
                                        [0.645434998334371],
                                        [0.637764702134504],
                                        [0.630030629995892],
                                        [0.622233555319305],
                                        [0.614374257805712],
                                        [0.606453523378315],
                                        [0.598472144103957],
                                        [0.590430918113913],
                                        [0.582330649524082],
                                        [0.574172148354573],
                                        [0.565956230448703],
                                        [0.557683717391417],
                                        [0.549355436427127],
                                        [0.540972220376989],
                                        [0.532534907555621],
                                        [0.524044341687276],
                                        [0.515501371821464],
                                        [0.506906852248053],
                                        [0.498261642411839], [0.4895666068266],
                                        [0.480822614988648],
                                        [0.472030541289883],
                                        [0.463191264930345],
                                        [0.454305669830306],
                                        [0.445374644541871],
                                        [0.436399082160126],
                                        [0.42737988023383],
                                        [0.418317940675659],
                                        [0.409214169672017],
                                        [0.40006947759242],
                                        [0.390884778898452],
                                        [0.381660992052332],
                                        [0.372399039425056],
                                        [0.363099847204168],
                                        [0.353764345301143],
                                        [0.34439346725839],
                                        [0.334988150155905],
                                        [0.32554933451756],
                                        [0.316077964217054],
                                        [0.306574986383523],
                                        [0.297041351306832],
                                        [0.287478012342544],
                                        [0.277885925816587],
                                        [0.268266050929618],
                                        [0.258619349661111],
                                        [0.248946786673153],
                                        [0.239249329213982],
                                        [0.229527947021264],
                                        [0.219783612225117],
                                        [0.210017299250899],
                                        [0.200229984721771],
                                        [0.190422647361027],
                                        [0.180596267894233],
                                        [0.170751828951145],
                                        [0.160890314967456],
                                        [0.151012712086344],
                                        [0.141120008059867],
                                        [0.131213192150184],
                                        [0.12129325503063], [0.11136118868665],
                                        [0.101417986316602],
                                        [0.0914646422324372],
                                        [0.0815021517602691],
                                        [0.0715315111408437],
                                        [0.0615537174299131],
                                        [0.0515697683985346],
                                        [0.0415806624332905],
                                        [0.0315873984364539],
                                        [0.021590975726096],
                                        [0.0115923939361583],
                                        [0.00159265291648683]],
                                  "train_indices": [8, 13, 44, 48, 58, 67, 69,
                                                    70, 71, 75, 77, 83, 102,
                                                    112, 127, 130, 143, 164,
                                                    166, 188, 214, 219, 223,
                                                    228, 240, 243, 257, 260,
                                                    286, 301, 308],
                                  "test_indices": [0, 1, 2, 3, 4, 5, 6, 7, 9,
                                                   10, 11, 12, 14, 15, 16, 17,
                                                   18, 19, 20, 21, 22, 23, 24,
                                                   25, 26, 27, 28, 29, 30, 31,
                                                   32, 33, 34, 35, 36, 37, 38,
                                                   39, 40, 41, 42, 43, 45, 46,
                                                   47, 49, 50, 51, 52, 53, 54,
                                                   55, 56, 57, 59, 60, 61, 62,
                                                   63, 64, 65, 66, 68, 72, 73,
                                                   74, 76, 78, 79, 80, 81, 82,
                                                   84, 85, 86, 87, 88, 89, 90,
                                                   91, 92, 93, 94, 95, 96, 97,
                                                   98, 99, 100, 101, 103, 104,
                                                   105, 106, 107, 108, 109,
                                                   110, 111, 113, 114, 115,
                                                   116, 117, 118, 119, 120,
                                                   121, 122, 123, 124, 125,
                                                   126, 128, 129, 131, 132,
                                                   133, 134, 135, 136, 137,
                                                   138, 139, 140, 141, 142,
                                                   144, 145, 146, 147, 148,
                                                   149, 150, 151, 152, 153,
                                                   154, 155, 156, 157, 158,
                                                   159, 160, 161, 162, 163,
                                                   165, 167, 168, 169, 170,
                                                   171, 172, 173, 174, 175,
                                                   176, 177, 178, 179, 180,
                                                   181, 182, 183, 184, 185,
                                                   186, 187, 189, 190, 191,
                                                   192, 193, 194, 195, 196,
                                                   197, 198, 199, 200, 201,
                                                   202, 203, 204, 205, 206,
                                                   207, 208, 209, 210, 211,
                                                   212, 213, 215, 216, 217,
                                                   218, 220, 221, 222, 224,
                                                   225, 226, 227, 229, 230,
                                                   231, 232, 233, 234, 235,
                                                   236, 237, 238, 239, 241,
                                                   242, 244, 245, 246, 247,
                                                   248, 249, 250, 251, 252,
                                                   253, 254, 255, 256, 258,
                                                   259, 261, 262, 263, 264,
                                                   265, 266, 267, 268, 269,
                                                   270, 271, 272, 273, 274,
                                                   275, 276, 277, 278, 279,
                                                   280, 281, 282, 283, 284,
                                                   285, 287, 288, 289, 290,
                                                   291, 292, 293, 294, 295,
                                                   296, 297, 298, 299, 300,
                                                   302, 303, 304, 305, 306,
                                                   307, 309, 310, 311, 312,
                                                   313, 314], "train_pool": {
            "__deque__": [8, 13, 44, 48, 58, 67, 69, 70, 71, 75, 77, 83, 102,
                          112, 127, 130, 143, 164, 166, 188, 214, 219, 223,
                          228, 240, 243, 257, 260, 286, 301, 308]},
                                  "test_pool": {
                                      "__deque__": [0, 1, 2, 3, 4, 5, 6, 7, 9,
                                                    10, 11, 12, 14, 15, 16, 17,
                                                    18, 19, 20, 21, 22, 23, 24,
                                                    25, 26, 27, 28, 29, 30, 31,
                                                    32, 33, 34, 35, 36, 37, 38,
                                                    39, 40, 41, 42, 43, 45, 46,
                                                    47, 49, 50, 51, 52, 53, 54,
                                                    55, 56, 57, 59, 60, 61, 62,
                                                    63, 64, 65, 66, 68, 72, 73,
                                                    74, 76, 78, 79, 80, 81, 82,
                                                    84, 85, 86, 87, 88, 89, 90,
                                                    91, 92, 93, 94, 95, 96, 97,
                                                    98, 99, 100, 101, 103, 104,
                                                    105, 106, 107, 108, 109,
                                                    110, 111, 113, 114, 115,
                                                    116, 117, 118, 119, 120,
                                                    121, 122, 123, 124, 125,
                                                    126, 128, 129, 131, 132,
                                                    133, 134, 135, 136, 137,
                                                    138, 139, 140, 141, 142,
                                                    144, 145, 146, 147, 148,
                                                    149, 150, 151, 152, 153,
                                                    154, 155, 156, 157, 158,
                                                    159, 160, 161, 162, 163,
                                                    165, 167, 168, 169, 170,
                                                    171, 172, 173, 174, 175,
                                                    176, 177, 178, 179, 180,
                                                    181, 182, 183, 184, 185,
                                                    186, 187, 189, 190, 191,
                                                    192, 193, 194, 195, 196,
                                                    197, 198, 199, 200, 201,
                                                    202, 203, 204, 205, 206,
                                                    207, 208, 209, 210, 211,
                                                    212, 213, 215, 216, 217,
                                                    218, 220, 221, 222, 224,
                                                    225, 226, 227, 229, 230,
                                                    231, 232, 233, 234, 235,
                                                    236, 237, 238, 239, 241,
                                                    242, 244, 245, 246, 247,
                                                    248, 249, 250, 251, 252,
                                                    253, 254, 255, 256, 258,
                                                    259, 261, 262, 263, 264,
                                                    265, 266, 267, 268, 269,
                                                    270, 271, 272, 273, 274,
                                                    275, 276, 277, 278, 279,
                                                    280, 281, 282, 283, 284,
                                                    285, 287, 288, 289, 290,
                                                    291, 292, 293, 294, 295,
                                                    296, 297, 298, 299, 300,
                                                    302, 303, 304, 305, 306,
                                                    307, 309, 310, 311, 312,
                                                    313, 314]}}}
                                                    """

    network = FFBPNetwork(1, 1)
    sin_encoded = decode_file(sin_json)
    network.train(sin_encoded, 3001, verbosity=0)
    network.test(sin_encoded)


if __name__ == '__main__':
    main()
