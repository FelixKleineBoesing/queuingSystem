import inspect
import copy
from typing import Union
from typeguard import check_type


def annotation_type_checker(func):
    """
    this decorator can be used for automatic type checking of the function arguments

    :param func:
    :return:
    """
    args_spec = inspect.getfullargspec(func)
    all_args, annotations, defaults_tuple = args_spec[0], args_spec[-1], args_spec[-4]
    if defaults_tuple is not None:
        defaults = dict(zip(reversed(all_args), reversed(defaults_tuple)))
    else:
        defaults = {}

    def wrapper(*args, **kwargs):
        new_args, all_new_args = _get_args_without_self(args, func, all_args)
        key_args = _create_only_keyword_arguments(args=new_args, kwargs=kwargs,
                                                  arg_names=all_new_args, annotations=annotations)
        for arg, value in key_args.items():
            if defaults.get(arg) is None:
                continue
            _assert_type(annotation=annotations[arg], arg=arg, value=value)
        res = func(*args, **kwargs)
        if "return" in annotations:
            _assert_type(annotation=annotations["return"], arg="return", value=res)
        return res

    wrapper.__signature__ = inspect.signature(func)

    return wrapper


def _assert_type(annotation, arg, value):
    """
    checks whether the annotation is an union or a single type.
    In that case it iterates over all types that are defined in the Union and checks whether
    the type of value is one of the types in Union.
    :param annotation: annotation from inspect.getfullargspec
    :param arg: name of argument
    :param value: supplied value for arg
    :return:
    """
    if _check_if_arg_is_union(annotation=annotation):
        fits = False
        for type_ in annotation.__args__:
            if type(value) == type:
                fits = fits or isinstance(value, type_)
            else:
                try:
                    check_type("arg", value, type_)
                    fit = True
                except TypeError as e:
                    fit = False
                except Exception as e:
                    raise Exception(e)
                fits = fits or fit
        if not fits:
            raise AssertionError(_get_assert_message(arg, annotation, type(value)))
    else:
        assert isinstance(value, annotation), _get_assert_message(arg, annotation, type(value))


def _create_only_keyword_arguments(args, kwargs, arg_names, annotations):
    """
    converts positional arguments into keyword arguments
    :param args:
    :param kwargs:
    :param arg_names:
    :return:
    """
    supplied_args = arg_names[:len(args)]
    key_args = copy.deepcopy(kwargs)
    key_args.update({key: value for key, value in zip(supplied_args, args)})
    key_args = {key: value for key, value in key_args.items() if key in annotations}
    return key_args


def _get_args_without_self(args, func, all_args):
    """
    this function detects whether the decorated function is a method of some class or object.
    if it´s the case the self argument will be removed
    :param args:
    :param func:
    :return:
    """
    if len(args) == 0:
        return args, all_args
    else:
        if not hasattr(args[0], "__class__"):
            return args, all_args
        if not args[0].__class__.__name__ in str(func):
            return args, all_args
        if not hasattr(args[0], func.__name__):
            return args, all_args
    return args[1:], all_args[1:]


def _get_assert_message(arg: str, annotation_type: Union[str, type], arg_type: Union[type, str]):
    """
    creates a assert message for type hinting
    :param arg:
    :param annotation_type:
    :param arg_type:
    :return:
    """
    return "Argument {0} must be an instance of {1}, but is of type {2}".format(arg, str(annotation_type),
                                                                                str(arg_type))


def _check_if_arg_is_union(annotation):
    """
    This function checks whether the annotation is a Union. Therefore it tries to access the attribute _name from
        attribute __origin__. If this isn´t accessible, the annotation is no Union! If it is another type of typing
        but name is not Union, it is neither an Union!
    :param annotation: annotation from function type hinting
    :return:
    """
    try:
        return annotation.__origin__._name == "Union"
    except:
        return False