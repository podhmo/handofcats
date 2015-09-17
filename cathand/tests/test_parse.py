# -*- coding:utf-8 -*-
import unittest


class TestIterateFunction(unittest.TestCase):
    def _getTargetClass(self):
        from cathand import CommandFromFunction
        return CommandFromFunction

    def _makeOne(self, fn):
        import inspect
        argspec = inspect.getargspec(fn)
        return self._getTargetClass()(fn, argspec)

    def test_iterate_positionals(self):
        def f(x, y, z):
            pass

        target = self._makeOne(f)
        result = list(target._iterate_positionals())
        self.assertEqual(["x", "y", "z"], result)

    def test_iterate_positionals2(self):
        def f(x, y, z=None, flag=False, **kwargs):
            pass

        target = self._makeOne(f)
        result = list(target._iterate_positionals())
        self.assertEqual(["x", "y"], result)

    def test_iterate_optionals(self):
        def f(a=True, b=None, c=False, **kwargs):
            pass

        target = self._makeOne(f)
        result = list(target._iterate_optionals())
        self.assertEqual([("a", True), ("b", None), ("c", False)], result)

    def test_iterate_optionals2(self):
        def f(x, y, z=None, flag=False, **kwargs):
            pass

        target = self._makeOne(f)
        result = list(target._iterate_optionals())
        self.assertEqual([("z", None), ("flag", False)], result)
