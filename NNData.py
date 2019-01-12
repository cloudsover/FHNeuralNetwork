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
        # TODO check that the lengths of x any y are the same otherwise
        #  raise datamismatch

        # TODO Assign x and y to the corresponding internal objects self.x
        #  and self.y

        # TODO Call the method split_set()
        pass

    def split_set(self, new_train_percentage=None):
        # TODO Docs

        # TODO reassign self.train_percentage if new_train_percentage is not
        #  None. -> Use the limiter

        # TODO Calculate the size of the training set and testing set using
        #  self.train_percentage and the size of the loaded data

        # TODO populate train_indices and test_indices with appropriately
        #  sized lists of indices to examine the data. The indices should be
        #  assigned randomly

        # TODO Call method prime_data()
        pass

    def prime_data(self, my_set=None, order=None):
        # TODO Docs

        # TODO if order is None, set order = NNData.Order.SEQUENTIAL.

        # TODO Copy test_indices to test_pool and train_indices to
        #  train_pool (or just one if my_set is specified as either Set.TEST
        #  or Set.TRAIN) Both test pools should be dequeues. If
        #  order=Order.RANDOM, the indices should be randomized as they are
        #  copied. Otherwise they should remain in their original order.
        pass

    def empty_pool(self, my_set=None):
        # TODO Docs

        # TODO If my_set is None, set my_set = NNData.Set.TRAIN.

        # TODO Return True if the pool indicated by my_set is empty,
        #  or False if not.
        pass

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
        print("There are errors that likely come from __init__ or a method called by __init__")
        errors = True
    try:
        our_data.split_set(30)
        assert len(our_data.train_indices) == 3
        assert len(our_data.test_indices) == 7
        assert (list(set(our_data.train_indices + our_data.test_indices))) == list(range(10))
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
        print("There are errors that may come from prime_data, but could be from another method")
        errors = True
    if errors:
        print("You have one or more errors.  Please fix them before submitting")
    else:
        print("No errors were identified by the unit test.")
        print("You should still double check that your code meets spec.")
        print("You should also check that PyCharm does not identify any PEP-8 issues.")

if __name__ == "__main__":
    main()
