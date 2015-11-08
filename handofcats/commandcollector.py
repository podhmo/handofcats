# -*- coding:utf-8 -*-
import logging
import glob
import os.path
from importlib import import_module

logger = logging.getLogger(__name__)


class ModuleScanner(object):
    def get_module_and_pathlist(self, module_or_path, importer):
        if hasattr(module_or_path, "__path__"):
            return module_or_path, module_or_path.__path__
        else:
            module = importer(module_or_path)
            return module, module.__path__

    def scan(self, root, exclude=None):
        logging.info("scan: %s", root)
        m, pathlist = self.get_module_and_pathlist(root, importer=import_module)
        root_package = m.__package__ or m.__name__
        for path in pathlist:
            logging.debug("scan path: %s", path)
            for target in glob.glob(os.path.join(path, "*.py")):
                if target.endswith("/__init__.py"):
                    target = target.replace("/__init__.py", "")
                if target == path:
                    continue
                if exclude and exclude(target):
                    continue
                logger.debug("scan target: %s", target)
                if target.endswith(".py"):
                    target = target[:-3]
                module = target.replace(path, root_package).replace(os.sep, ".")
                logger.info("scan command: %s", module)
                yield module


class CommandCollector(object):
    def __init__(self):
        self.managed_set = set()
        self.scanner = ModuleScanner()

    def mark(self, target):
        self.managed_set.add(target)
        return target

    def is_marked(self, target):
        return target in self.managed_set

    def collect(self):
        return self.managed_set

    def scan(self, root, exclude=None):
        for module in self.scanner.scan(root, exclude=exclude):
            import_module(module)
        return self.collect()
