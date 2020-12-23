import abc


class Arguments(abc.ABC):

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def check_if_item_has_attr(self, item):
        return hasattr(self, item)