import sys
import inspect


def gather_imported_classes(module=sys.modules[__name__], base_class=None):
    """
    gather all classes that are imported inside a module. If you want, you can specify the base class by which the
    classes should be filtered

    :param module: module  in which you import those classes
    :param base_class: class from all returned classes should be inherited
    :return:
    """
    objects = inspect.getmembers(module, predicate=inspect.isclass)
    classes = []
    for name, obj in objects:
        if base_class is not None:
            if obj.__base__ is base_class:
                classes.append(obj)
    return classes
