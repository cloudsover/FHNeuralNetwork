from enum import Enum, auto


class NNData:
    """This class is the first part of an artificial neural network written
    in python. It takes in two parts of the same data set as well as a
    percentage of data to be used in training set


    """
    DEFAULT_PERCENTAGE = 100

    def __init__(self, percentage: int = DEFAULT_PERCENTAGE, x: list = None,
                 y: list = None):
        """
        Constructor Method
        Args:
            percentage: percentage of data to be used in training set
            x: example part of data set
            y: label part of data set
        Raises:
            DataMismatchError
        """

        # Initializes x and y lists if not provided
        if x is None:
            x = []
        if y is None:
            y = []

        # Raise error if set sizes do not match
        if len(x) != len(y):
            raise DataMismatchError

        # Filter given percentage data through mutator method
        self.train_percentage = NNData.percentage_limiter(percentage)

        # Setting most internal data to None to avoid errors at this time
        self.x = None
        self.y = None
        self.train_indices = None
        self.train_pool = None
        self.test_indices = None
        self.test_pool = None

        # Calls place-holder method
        NNData.load_data(self)

    @staticmethod
    def percentage_limiter(percentage: int) -> int:
        """
        Filters the data given.

        Args:
            percentage: An int representing the percentage of data to be
            used.

        Returns:
            The given value, if between 0 and 100.
            If the value of percentage is below 0, returns 0.
            If the value of percentage is above 100, returns 100.

        Raises:
            DataMismatchError: An error occurred because the function wasn't
            able to pass an int through it's filter.
        """
        try:
            percentage = int(percentage)
        except DataMismatchError:
            raise DataMismatchError

        # Mutates Values to upper or lower bounds if bad data is passed
        if percentage < 0:
            return 0
        if percentage > 100:
            return 100
        else:
            return percentage

    def load_data(self):
        """ Method-stub placeholder"""
        pass

    # Inner Order Class ------------------------------------------------------
    class Order(Enum):
        """Enum which determines whether the training data is presented in
        the same order to the neural network each time, or in a random order

        Returns:
            RANDOM: Indicates that training data is presented in random order.

            SEQUENTIAL: Indicates that training data is presented in
            sequential order.
        """
        RANDOM = auto()
        SEQUENTIAL = auto()

    # Inner Set Class ------------------------------------------------------
    class Set(Enum):
        """Enum which helps to identify whether we are requesting training
        set data or testing set data
        Returns:
            TRAIN: Identifies that training data is requested.

            TEST: Identifies that testing data is requested.
        """
        TRAIN = auto()
        TEST = auto()


class DataMismatchError(Exception):
    """Custom Exception"""
    pass


def main():
    errors = False
    test = NNData()
    test2 = NNData(percentage=110)
    test3 = NNData(percentage=-10)
    test4 = NNData(percentage=30)
    try:
        assert isinstance(test.Order.RANDOM, Enum)
        assert isinstance(test.Order.SEQUENTIAL, Enum)
        assert isinstance(test.Set.TRAIN, Enum)
        assert isinstance(test.Set.TEST, Enum)
    except:
        print("Enums are not properly established")
        errors = True
    try:
        assert test.train_percentage == 100
        assert test2.train_percentage == 100
        assert test3.train_percentage == 0
        assert test4.train_percentage == 30
    except:
        print("train_percentage not properly handled")
        errors = True
    try:
        try:
            raise DataMismatchError
        except DataMismatchError:
            pass
        except:
            print("DataMismatchError not properly established")
            errors = True
    except:
        print("DataMismatchError not properly established")
        errors = True
    if errors:
        print(
            "You have one or more errors.  Please fix them before submitting")
    else:
        print("No errors were identified by the unit test.")
        print("You should still double check that your code meets spec.")
        print("You should also check that PyCharm does not identify any "
              "PEP-8 issues.")


if __name__ == "__main__":
    main()
