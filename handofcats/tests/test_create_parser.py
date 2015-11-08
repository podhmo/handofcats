# -*- coding:utf-8 -*-
import unittest
import contextlib


@contextlib.contextmanager
def mustcall(self, status=True):
    called = [False]

    def activate():
        called[0] = True
    yield activate
    self.assertEqual(called[0], status)


class TestCreatParser(unittest.TestCase):
    def _getTargetClass(self):
        from handofcats.commandcreator import CommandFromFunction
        return CommandFromFunction

    def _makeOne(self, positionals, optionals, fn):
        import inspect
        Class = self._getTargetClass()

        class CommandFromFunction(Class):
            def _iterate_positionals(self):
                return positionals

            def _iterate_optionals(self):
                return optionals
        argspec = inspect.getargspec(fn)
        return CommandFromFunction(fn, argspec)

    def test_it(self):
        positionals = ["file"]
        optionals = [("x", False), ("y", True), ("foo", "foo")]

        with mustcall(self) as activate:
            def f(file, x=False, y=True, foo="foo"):
                self.assertEqual(file, "input-file")
                self.assertEqual(x, False)
                self.assertEqual(y, True)
                self.assertEqual(foo, "foo")
                activate()

            target = self._makeOne(positionals, optionals, f)
            target.run_as_command(["input-file"])

    def test_it__positional_paramaters_are_not_enough(self):
        positionals = ["file"]
        optionals = [("x", False), ("y", True), ("foo", "foo")]

        with mustcall(self, status=False) as activate:
            def f(file, x=False, y=True, foo="foo"):
                self.assertEqual(file, "input-file")
                self.assertEqual(x, False)
                self.assertEqual(y, True)
                self.assertEqual(foo, "foo")
                activate()

            target = self._makeOne(positionals, optionals, f)

            with self.assertRaises(SystemExit):
                target.run_as_command([])

    def test_it__with_paramater(self):
        positionals = ["file"]
        optionals = [("x", False), ("y", True), ("foo", "foo")]

        with mustcall(self) as activate:
            def f(file, x=False, y=True, foo="foo"):
                self.assertEqual(file, "input-file")
                self.assertEqual(x, True)
                self.assertEqual(y, False)
                self.assertEqual(foo, "bar")
                activate()

            target = self._makeOne(positionals, optionals, f)
            target.run_as_command(["--x", "--y", "--foo=bar", "input-file"])

    def test_it__with_paramater2(self):
        positionals = ["file"]
        optionals = [("intnum", 0), ("floatnum", 0.1), ("foo", "foo")]

        with mustcall(self) as activate:
            def f(file, intnum=0, floatnum=0.1, foo="foo"):
                self.assertEqual(foo, "bar")
                self.assertEqual(intnum, 10)
                self.assertEqual(floatnum, 0.1)
                activate()

            target = self._makeOne(positionals, optionals, f)
            target.run_as_command(["--foo", "bar", "--intnum", "10", "input-file"])

    def test_it_with_underscore(self):
        positionals = ["file_name"]
        optionals = [("int_num", 1), ("_float_num", 0.1)]

        with mustcall(self) as activate:
            def f(file, int_num=0, float_num=0.0):
                self.assertEqual(int_num, 1)
                self.assertEqual(float_num, 0.1)
                activate()

            target = self._makeOne(positionals, optionals, f)
            target.run_as_command(["--int-num", "1", "--float-num", "0.1", "input-file"])
