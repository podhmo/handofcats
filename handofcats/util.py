import sys
from logging import getLogger as get_logger
from importlib import (
    import_module,
    machinery,
)
logger = get_logger(__name__)


def _import_symbol_from_module(module, name, logger=logger):
    logger.debug("import module=%s, name=%s", module, name)
    module = import_module(module)
    return getattr(module, name)


def _import_symbol_from_filepath(path, name, module_id=None, logger=logger):
    logger.debug("import path=%s, name=%s", path, name)
    module_id = module_id or path.replace("/", "_").rstrip(".py")
    module = machinery.SourceFileLoader(module_id, path).load_module()
    return getattr(module, name)


def import_symbol(path, sep=":", logger=logger):
    try:
        module, name = path.rsplit(sep, 1)
        return _import_symbol_from_module(module, name, logger=logger)
    except ImportError:
        sys.path.append(".")
        return _import_symbol_from_filepath(module, name, logger=logger)
