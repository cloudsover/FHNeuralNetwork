"""

Assignment Two: Building a Data Class
Eric Reed

Complete the NNData class to hold and manage data for our
neural network
- implement load_data(), split_set(), prime_data(), empty_pool()
  get_number_samples() and get_one_item()

"""

import random
import math
import collections
from enum import Enum


class DataMismatchError(Exception):
    """ number of X and Y elements do not match"""
    pass

    class Order(Enum):
        RANDOM = 0
        SEQUENTIAL = 1

    class Set(Enum):
        TRAIN = 0
        TEST = 1


class NNData:

    def __init__(self, x=None, y=None, train_percentage=100):

        if x is None:
            x = []
        if y is None:
            y = []
        self.train_percentage = NNData.percentage_limiter(train_percentage)
        self.x = None
        self.y = None
        self.train_indices = None
        self.test_indices = None
        self.train_pool = None
        self.test_pool = None
        self.load_data(x, y)
        pass

    def load_data(self, x, y):
        if len(x) != len(y):
            raise DataMismatchError()
        self.x = x
        self.y = y
        self.split_set()

    def split_set(self, new_train_percentage=None):
        if new_train_percentage is not None:
            self.train_percentage = NNData.percentage_limiter(
                new_train_percentage)
        total_set_size = len(self.x)
        train_set_size = math.floor(
            total_set_size * self.train_percentage / 100)
        self.train_indices = random.sample(range(total_set_size),
                                           train_set_size)
        self.test_indices = list(
            set(range(total_set_size)) - set(self.train_indices))
        self.train_indices.sort()
        self.prime_data()

    def get_one_item(self, my_set=None):
        if my_set is None:
            my_set = NNData.Set.TRAIN
        try:
            if my_set == NNData.Set.TRAIN:
                index = self.train_pool.popleft()
            else:
                index = self.test_pool.popleft()
            return self.x[index], self.y[index]
        except IndexError:
            return None

    def get_number_samples(self, my_set=None):
        if my_set is NNData.Set.TEST:
            return len(self.test_indices)
        elif my_set is NNData.Set.TRAIN:
            return len(self.train_indices)
        else:
            return len(self.x)

    def empty_pool(self, my_set=None):
        if my_set is None:
            my_set = NNData.Set.TRAIN
        if my_set is NNData.Set.TRAIN:
            if len(self.train_pool) == 0:
                return True
            else:
                return False
        else:
            if len(self.test_pool) == 0:
                return True
            else:
                return False

    def prime_data(self, my_set=None, order=None):
        if order is None:
            order = NNData.Order.SEQUENTIAL
        if my_set is not NNData.Set.TRAIN:
            test_indices_temp = list(self.test_indices)
            if order == NNData.Order.RANDOM:
                random.shuffle(test_indices_temp)
            self.test_pool = collections.deque(test_indices_temp)
        if my_set is not NNData.Set.TEST:
            train_indices_temp = list(self.train_indices)
            if order == NNData.Order.RANDOM:
                random.shuffle(train_indices_temp)
            self.train_pool = collections.deque(train_indices_temp)

    @staticmethod
    def percentage_limiter(percentage):
        return min(100, max(percentage, 0))
