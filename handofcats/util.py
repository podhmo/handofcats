import sys
from logging import getLogger as get_logger
from importlib import (
    import_module,
    machinery,
)
logger = get_logger(__name__)


# stolen from pyramid
class reify(object):
    """cached property"""

    def __init__(self, wrapped):
        self.wrapped = wrapped
        try:
            self.__doc__ = wrapped.__doc__
        except:
            pass

    def __get__(self, inst, objtype=None):
        if inst is None:
            return self
        val = self.wrapped(inst)
        setattr(inst, self.wrapped.__name__, val)
        return val


def _import_symbol_from_module(module, name, logger=logger):
    logger.debug("import module=%s, name=%s", module, name)
    module = import_module(module)
    return getattr(module, name)


def _import_symbol_from_filepath(path, name, module_id=None, logger=logger):
    logger.debug("import path=%s, name=%s", path, name)
    module_id = module_id or path.replace("/", "_")
    if module_id.endswith(".py"):
        module_id = module_id[:-3]
    module = machinery.SourceFileLoader(module_id, path).load_module()
    return getattr(module, name)


def import_symbol(path, sep=":", logger=logger):
    try:
        module, name = path.rsplit(sep, 1)
        return _import_symbol_from_module(module, name, logger=logger)
    except (ImportError, TypeError):
        sys.path.append(".")
        return _import_symbol_from_filepath(module, name, logger=logger)
