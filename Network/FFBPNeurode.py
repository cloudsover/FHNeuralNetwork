from Network.BPNeurode import BPNeurode
from Network.FFNeurode import FFNeurode
from Network.LayerType import LayerType


class FFBPNeurode(BPNeurode, FFNeurode):
    """
    FFBNPNeurode merges the functionality of both the BPNeurode and the
    FFNeurode.
    """

    def __init__(self, my_type: LayerType = LayerType.INPUT):
        """
        Inits FFBPNeurode with all inherited attributes initialized

        Args:
            my_type: LayerType enum. Determines the layer classification of
            the neurode.
        """
        super().__init__(my_type)


def main():
    print("These tests depend on your prior work.")
    print("Be sure you have either imported assignments 2, 4 and 5 or include them in the same file as assignment 6.")
    try:
        test_neurode = BPNeurode(0)
    except:
        print("Error - Cannot instaniate a BPNeurode object")
        return
    print("Testing Sigmoid Derivative")
    try:
        assert BPNeurode.sigmoid_derivative(0) == 0
        if test_neurode.sigmoid_derivative(.4) == .24:
            print("Pass")
        else:
            print("sigmoid_derivative is not returning the correct result")
    except:
        print("Error - Is sigmoid_derivative named correctly, created in BPNeurode and decorated as a static method?")
    print("Testing Instance objects")
    try:
        test_neurode.learning_rate
        test_neurode.delta
        print("Pass")
    except:
        print("Error - Are all instance objects created in __init__()?")

    inodes = []
    hnodes = []
    onodes = []
    for k in range(2):
        inodes.append(FFBPNeurode(LayerType.INPUT))
        hnodes.append(FFBPNeurode(LayerType.HIDDEN))
        onodes.append(FFBPNeurode(LayerType.OUTPUT))
    for node in inodes:
        node.clear_and_add_output_nodes(hnodes)
    for node in hnodes:
        node.clear_and_add_input_nodes(inodes)
        node.clear_and_add_output_nodes(onodes)
    for node in onodes:
        node.clear_and_add_input_nodes(hnodes)
    print("Testing register_back_input")
    try:
        hnodes[0].reporting_outputs = 1
        if hnodes[0].register_back_input(onodes[1]) and not hnodes[1].register_back_input(onodes[1]):
            print("Pass")
        else:
            print("Error - register_back_input is not responding correctly")
    except:
        print("Error - register_back_input is raising an error.  Is it named correctly?  Check your syntax")
    print("Testing calculate_delta on output nodes")
    try:
        onodes[0].value = .2
        onodes[0].calculate_delta(.5)
        if .0479 < onodes[0].delta < .0481:
            print("Pass")
        else:
            print("Error - calculate delta is not returning the correct value.  Check the math.")
            print("        Hint: do you have a separate process for hidden nodes vs output nodes?")
    except:
        print("Error - calculate_delta is raising an error.  Is it named correctly?  Check your syntax")
    print("Testing calculate_delta on hidden nodes")
    try:
        onodes[0].delta = .2
        onodes[1].delta = .1
        onodes[0].input_nodes[hnodes[0]] = .4
        onodes[1].input_nodes[hnodes[0]] = .6
        hnodes[0].value = .3
        hnodes[0].calculate_delta()
        if .02939 < hnodes[0].delta < .02941:
            print("Pass")
        else:
            print("Error - calculate delta is not returning the correct value.  Check the math.")
            print("        Hint: do you have a separate process for hidden nodes vs output nodes?")
    except:
        print("Error - calculate_delta is raising an error.  Is it named correctly?  Check your syntax")
    try:
        print("Testing update_weights")
        hnodes[0].update_weights()
        #hnodes[1].update_weights()

        if onodes[0].learning_rate == .05:
            if .4 + .06 * onodes[0].learning_rate - .001 < onodes[0].input_nodes[hnodes[0]] \
                    < .4 + .06 * onodes[0].learning_rate + .001:
                print("Pass")
            else:
                print("Error - weights not updated correctly.  If all other methods passed, check update_weights")
        else:
            print("Error - Learning rate should be .05, please verify")
    except:
        print("Error - update_weights is raising an error.  Is it named correctly?  Check your syntax")
    print("All that looks good.  Trying to train a trivial dataset on our network")
    inodes = []
    hnodes = []
    onodes = []
    for k in range(2):
        inodes.append(FFBPNeurode(LayerType.INPUT))
        hnodes.append(FFBPNeurode(LayerType.HIDDEN))
        onodes.append(FFBPNeurode(LayerType.OUTPUT))
    for node in inodes:
        node.clear_and_add_output_nodes(hnodes)
    for node in hnodes:
        node.clear_and_add_input_nodes(inodes)
        node.clear_and_add_output_nodes(onodes)
    for node in onodes:
        node.clear_and_add_input_nodes(hnodes)
    inodes[0].receive_input(None, 1)
    inodes[1].receive_input(None, 0)
    value1 = onodes[0].get_value()
    value2 = onodes[1].get_value()
    onodes[0].receive_back_input(None, 0)
    onodes[1].receive_back_input(None, 1)
    inodes[0].receive_input(None, 1)
    inodes[1].receive_input(None, 0)
    value1a = onodes[0].get_value()
    value2a = onodes[1].get_value()
    if (value1 - value1a > 0) and (value2a - value2 > 0):
        print("Pass - Learning was done!")
    else:
        print("Fail - the network did not make progress.  If everything else passed, first try these hints:")
        print("    Hint1: Check receive_back_input()")
        print("    Hint2: Check back_fire(), especially the order of method calls")
        print("If you hit a wall, be sure to seek help in the discussion form, from the instructor and from the tutors")
if __name__ == "__main__":
    main()
