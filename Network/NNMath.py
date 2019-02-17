import numpy as np


def y_hat_formula(x_list, y_list):
    """TODO Docs"""
    x_list = np.array(x_list)
    y_list = np.array(y_list)
    denominator = x_list.dot(x_list) - x_list.mean() * x_list.sum()
    a = a_formula(x_list, y_list, denominator)
    b = b_formula(x_list, y_list, denominator)
    return a * x_list + b


def y_hat_denominator(x_list: np.array):
    """TODO Docs"""
    return x_list.dot(x_list) - x_list.mean() * x_list.sum()


def a_formula(x_list: np.array, y_list: np.array, denominator: float):
    """TODO Docs"""
    x_list = np.array(x_list)
    y_list = np.array(y_list)

    a = (x_list.dot(y_list)
         - y_list.mean()
         * x_list.sum()) \
        / denominator
    return a


def b_formula(x_list: np.array, y_list: np.array, denominator: float):
    """TODO Docs"""
    b = (y_list.mean()
         * x_list.dot(x_list)
         - x_list.mean()
         * x_list.dot(y_list)) \
        / denominator
    return b


def mse_formula(x_list, y_list):
    """TODO Docs"""
    y_hat = y_hat_formula(x_list, y_list)

    mse = 0
    n = len(y_list)
    for i in range(n):
        mse += np.exp(i - y_hat, 2)
    return mse / n

# TODO migrate sigmoid
# TODO migrate sigmoid derivative
# TODO Add algorithms
