import inspect
from functools import wraps
from typing import Union, List

FloatList = Union[float, List[float]]
IntList = Union[int, List[int]]
ListIntList = Union[List[IntList], IntList]
ListFloatList = Union[List[FloatList], FloatList]


def check_length_list_equality(func):
    """
    if one parameter is a list they must all be list and have the same length. Otherwise the input is wrong
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if len(args) > 0:
            val = args[0]
        else:
            val = kwargs[list(kwargs.keys())[0]]
        if isinstance(val, list):
            length = len(val)
            for arg in list(args) + list(kwargs.values()):
                _check_if_equal_length(arg, length)
        else:
            for arg in list(args) + list(kwargs.values()):
                if not isinstance(arg, object):
                    assert not isinstance(arg, list), "if interval is not a list all other " \
                                                      "parameter may be no list either"
        res = func(*args, **kwargs)
        return res

    wrapper.__signature__ = inspect.signature(func)

    return wrapper


def _check_if_equal_length(arg: list, length: int):
    """
    checks if argument is of equal length and raises assertion error otherwise

    :param arg:
    :param length:
    :return:
    """
    assert isinstance(arg, list), "if one argument is of type list, all arguments must be of type list"
    assert length == len(arg), "Length of all arguments must be equal if of type list"

