import collections
from enum import Enum, auto
import random
import numpy as np


class NNData:
    """This class is the first part of an artificial neural network written
    in python. It takes in two parts of the same data set as well as a
    percentage of data to be used in training set


    """
    DEFAULT_PERCENTAGE = 100

    class Order(Enum):
        """Enum which determines whether the training data is presented in
        the same order to the neural network each time, or in a random order

        Returns:
            RANDOM: Indicates that training data is presented in random order.

            SEQUENTIAL: Indicates that training data is presented in
            sequential order.
        """
        RANDOM = 0
        SEQUENTIAL = 1

    class Set(Enum):
        """Enum which helps to identify whether we are requesting training
        set data or testing set data
        Returns:
            TRAIN: Identifies that training data is requested.

            TEST: Identifies that testing data is requested.
        """
        TRAIN = 0
        TEST = 1

    def __init__(self,
                 x: list = None,
                 y: list = None,
                 percentage: int = DEFAULT_PERCENTAGE):
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

        self.x: list = x  # example part of data - list of lists
        self.y: list = y  # label part of data - List of lists
        self.train_indices: list = None  # List of pointers to training subset
        self.train_pool: list = None  # dequeue containing examples not yet
        self.train_data: tuple = (self.train_indices, self.train_pool)

        self.test_indices: list = None  # List of pointers for testing subset
        self.test_pool: list = None  # dequeue containing examples not used in
        self.test_data: tuple = (self.test_indices, self.test_pool)

        # Filter given percentage data through mutator method
        self.train_percentage = NNData.percentage_limiter(percentage)

        # Initializes Data
        self.load_data(x, y)

    @staticmethod
    def percentage_limiter(percentage: int = DEFAULT_PERCENTAGE) -> int:
        """
        Filters the data given.

        Args:
            percentage: An int representing the percentage of data to be
            used.

        Returns:
            The given value, if between 0 and 100.
            If the value of percentage is below 0, returns 0.
            If the value of percentage is above 100, returns 100.
        """

        # Mutates Values to upper or lower bounds if bad data is passed

        return min(100, max(percentage, 0))

    def load_data(self, x: list = None, y: list = None):
        """ Checks that the lengths of x and y are the same. Calls the
        method split_set

        Args:
            x: example part of data - list of lists
            y: label part of data - List of lists
        Raises:
            DataMismatchError: Raised if x and y are not the same length.
            """
        if len(x) != len(y):
            raise DataMismatchError
        self.x = x
        self.y = y

        self.split_set()

    def split_set(self, new_train_percentage=None):
        """ Splits the data between the training and testing pools based on
        the percentage given.

        Populates train_indices and test_indices

        Calls prime.data()

        Args:
            new_train_percentage: new percentage value to set
            self.percentage to. Run through percentage_limiter()
        """

        if new_train_percentage is not None:
            self.train_percentage = self.percentage_limiter(
                new_train_percentage)

        # Setting lengths relative to the size of the data, and the
        # percentage of data to use in testing
        data_size = np.math.floor(len(self.x))
        train_size = np.math.floor(data_size * (self.train_percentage * 0.01))

        # Populating train and test indices which will point to example data
        self.train_indices = list(random.sample(range(0, data_size),
                                                train_size))
        self.test_indices = list(
            set(range(0, data_size)) - set(self.train_indices))

        self.prime_data(self)

    def prime_data(self, my_set=None, order=None):
        """ Copies indices into desired pools for training and testing.
        Default is both training and testing.

        Args:
            my_set: Specified if only one set is to be primed
            order: Specified if specific ordering is desired. Defaults to
            Sequential.
        """

        test_indices_temp = self.test_indices[:]
        train_indices_temp = self.train_indices[:]

        # Default ordering of data
        if order is None or order is self.Order.SEQUENTIAL:
            order = self.Order.SEQUENTIAL

        elif order is self.Order.RANDOM:
            random.shuffle(test_indices_temp)
            random.shuffle(train_indices_temp)

        # Only populate test set
        if my_set is self.Set.TEST:
            self.test_pool = collections.deque(test_indices_temp)

        # Only populate train set
        elif my_set is self.Set.TRAIN:
            self.train_pool = collections.deque(train_indices_temp)

        # Populate test and train pools with the example values pointed to
        # by the listed indices
        else:
            self.train_pool = collections.deque(train_indices_temp)
            self.test_pool = collections.deque(test_indices_temp)

    def empty_pool(self, my_set=None) -> bool:
        """ Checks to see if the specified set is empty, defaults to
        training set.

        Args:
            my_set: Specific set to check if empty.
        """

        if my_set is None:
            my_set = self.Set.TRAIN

        # Testing if training pool is empty
        if my_set is self.Set.TRAIN:
            if not self.train_pool:
                return True
            if self.train_pool:
                return False

        if not self.test_pool:
            return True
        if self.test_pool:
            return False

    def get_number_samples(self, my_set=None) -> int:
        """Returns the number of samples in the data set requested. Defaults
        to the entire set.
        Args:
            my_set: Specified data set. Either testing set or training set.
        Returns:
            Size of set as an int.
            """

        # If not specified, returns the size of the entire set
        if my_set is None:
            return len(self.x)

        # Size of training set
        if my_set is self.Set.TRAIN:
            return len(self.train_indices)

        # Size of testing set
        if my_set is self.Set.TEST:
            return len(self.test_indices)

    def get_one_item(self, my_set=None) -> list:
        """Pops one item from the indicated set and returns a list in the
        form of [x,y] x being the example data, and y is the corresponding
        label.
        """

        # Set default set to train
        if my_set is None:
            my_set = self.Set.TRAIN

        # Pop from train set
        if my_set is self.Set.TRAIN:
            index = self.train_pool.popleft()
            example = self.x[index]
            label = self.y[index]
            ret_item = [example, label]
            return ret_item

        # Pop from test set
        index = self.test_pool.popleft()
        example = self.x[index]
        label = self.y[index]
        ret_item = [example, label]
        return ret_item


class DataMismatchError(Exception):
    """Custom Exception"""
