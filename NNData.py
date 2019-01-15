import collections
from enum import Enum, auto
import random


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

        self.x = x
        self.y = y
        self.train_indices = None
        self.train_pool = None
        self.test_indices = None
        self.test_pool = None

        # Filter given percentage data through mutator method
        self.train_percentage = NNData.percentage_limiter(percentage)

        # Initializes Data
        NNData.load_data(self, x, y)

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
        """

        # Mutates Values to upper or lower bounds if bad data is passed
        if percentage < 0:
            return 0
        if percentage > 100:
            return 100
        else:
            return int(percentage)

    def load_data(self, x, y):
        # TODO Docs
        """ Method-stub placeholder"""

        if len(self.x) != len(self.y):
            raise DataMismatchError

        # TODO Comments
        self.x = x
        self.y = y

        NNData.split_set(self)
        pass

    def split_set(self, new_train_percentage=None):
        # TODO Docs

        # TODO Comments
        if new_train_percentage is not None:
            self.train_percentage = NNData.percentage_limiter(
                new_train_percentage)

        # Setting lengths relative to the size of the data, and the
        # percentage of data to use in testing
        train_size = (len(self.x) * (self.train_percentage * .01))
        data_size = len(self.x)

        # Populating train and test indices which will point to example data
        self.train_indices = random.sample(range(0, data_size), train_size)
        self.test_indices = list(
            set((range(0, data_size - set(self.train_indices)))))

        NNData.prime_data(self)

    def prime_data(self, my_set=None, order=None):
        # TODO Docs

        if order is None:
            order = NNData.Order.SEQUENTIAL

        # TODO Make this work
        if my_set is NNData.Set.TEST:
            self.test_pool = collections.deque()

        # TODO Make this work
        if my_set is NNData.Set.TRAIN:
            self.train_pool = collections.deque()

        # TODO Make this work
        else:
            self.test_pool = collections.deque()

            # TODO Make this work
        if order is NNData.Order.RANDOM:
            pass
        # TODO Copy test_indices to test_pool and train_indices to
        #  train_pool (or just one if my_set is specified as either Set.TEST
        #  or Set.TRAIN) Both test pools should be dequeues. If
        #  order=Order.RANDOM, the indices should be randomized as they are
        #  copied. Otherwise they should remain in their original order.
        pass

    def empty_pool(self, my_set=None):
        # TODO Docs

        if my_set is None:
            my_set = NNData.Set.TRAIN

        # TODO True if pool poined to by my_set is empty
        # TODO False if not empty

    def get_number_samples(self, my_set=None):
        # TODO Docs

        # TODO If my_set is None, return the total number of samples in the
        #  dataset.

        # TODO Otherwise, return the total number of samples in the set
        #  requested (TEST or TRAIN)

        pass

    def get_one_item(self, my_set=None):
        # TODO Docs

        # TODO if my_set is None, set my_set = NNData.Set.Train.

        # TODO popleft and return one item from the appropriate pool
        #  dequeue, or None if the requested pool is empty. The item
        #  returned should be a list of the form [x,y] where x is an example
        #  and y is the corresponding label (expected result)
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


# Unit Test
def main():
    errors = False
    try:
        X = list(range(10))
        Y = X
        our_data = NNData(X, Y)
        X = list(range(100))
        Y = X
        our_big_data = NNData(X, Y, 50)
        Y = [1]
        try:
            our_bad_data = NNData(X, Y)
            raise Exception
        except DataMismatchError:
            pass
        except:
            raise Exception
        X = ['a', 'b', 'c', 'd']
        Y = ['A', 'B', 'C', 'D']
        our_char_data = NNData(X, Y, 50)
    except:
        print(
            "There are errors that likely come from __init__ or a method called by __init__")
        errors = True
    try:
        our_data.split_set(30)
        assert len(our_data.train_indices) == 3
        assert len(our_data.test_indices) == 7
        assert (list(
            set(our_data.train_indices + our_data.test_indices))) == list(
            range(10))
    except:
        print("There are errors that likely come from split_set")
        errors = True
    try:
        our_data.prime_data(order=NNData.Order.SEQUENTIAL)
        assert len(our_data.train_pool) == 3
        assert len(our_data.test_pool) == 7
        assert our_data.train_indices == list(our_data.train_pool)
        assert our_data.test_indices == list(our_data.test_pool)
        our_big_data.prime_data(order=NNData.Order.RANDOM)
        assert our_big_data.train_indices != list(our_big_data.train_pool)
        assert our_big_data.test_indices != list(our_big_data.test_pool)
    except:
        print("There are errors that likely come from prime_data")
        errors = True

    try:
        our_data.prime_data(order=NNData.Order.SEQUENTIAL)
        my_x_list = []
        my_y_list = []
        while not our_char_data.empty_pool():
            example = our_char_data.get_one_item()
            my_x_list.append(example[0])
            my_y_list.append(example[1])
        assert len(my_x_list) == 2
        assert my_x_list != my_y_list
        my_upper_x_list = [k.upper() for k in my_y_list]
        assert my_upper_x_list == my_y_list
        while not our_char_data.empty_pool(our_char_data.Set.TEST):
            example = our_char_data.get_one_item(our_char_data.Set.TEST)
            my_x_list.append(example[0])
            my_y_list.append(example[1])
        assert my_x_list != my_y_list
        my_upper_x_list = [k.upper() for k in my_y_list]
        assert my_upper_x_list == my_y_list
        assert set(my_x_list) == set(X)
        assert set(my_y_list) == set(Y)
    except:
        print(
            "There are errors that may come from prime_data, but could be from another method")
        errors = True
    if errors:
        print(
            "You have one or more errors.  Please fix them before submitting")
    else:
        print("No errors were identified by the unit test.")
        print("You should still double check that your code meets spec.")
        print(
            "You should also check that PyCharm does not identify any PEP-8 issues.")


if __name__ == "__main__":
    main()
