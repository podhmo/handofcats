from functools import update_wrapper
from magicalimport import import_symbol  # noqa F401


# stolen from pyramid
class reify(object):
    """cached property"""

    def __init__(self, wrapped):
        self.wrapped = wrapped
        update_wrapper(self, wrapped)

    def __get__(self, inst, objtype=None):
        if inst is None:
            return self
        val = self.wrapped(inst)
        setattr(inst, self.wrapped.__name__, val)
        return val
