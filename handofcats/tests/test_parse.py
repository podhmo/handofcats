import unittest
import json


class Tests(unittest.TestCase):
    maxDiff = None

    def _getTargetFunction(self):
        from handofcats import as_command
        return as_command

    def _callFUT(self, fn, *, argv):
        target_function = self._getTargetFunction()

        from handofcats.driver import Driver
        from handofcats.parsers import testing

        class MyDriver(Driver):
            parser_factory = testing.create_parser

        return target_function(fn=fn, argv=argv, force=True, driver=MyDriver)

    def test_it(self):
        from handofcats.parsers.testing import ParseArgsCalled
        from collections import namedtuple

        C = namedtuple("C", "msg, fn, expected")
        _DEFAULT_INT = 100
        _DEFAULT_FLOAT = 0.12345
        _DEFAULT_STR = "*default*"

        def f_str(*, name: str) -> None:
            pass

        def f_str__short(*, x: str) -> None:
            pass

        def f_str__default_value(*, name: str = _DEFAULT_STR) -> None:
            pass

        def f_int(*, val: int) -> None:
            pass

        def f_int__default_value(*, val: int = _DEFAULT_INT) -> None:
            pass

        def f_float(*, val: float) -> None:
            pass

        def f_float__default_value(*, val: float = _DEFAULT_FLOAT) -> None:
            pass

        def f_bool(*, verbose: bool) -> None:
            pass

        def f_bool__default_is_true(*, verbose: bool = True) -> None:
            pass

        # yapf: disable
        candidates = [
            C(
                msg="(name:str), must be --name",
                fn=f_str,
                expected=[
                    {'name': 'add_argument', 'args': ('--name',), 'kwargs': {'required': True}},
                ],
            ),
            C(
                msg="(x:str), short option, must be -x",
                fn=f_str__short,
                expected=[
                    {'name': 'add_argument', 'args': ('-x',), 'kwargs': {'required': True}},
                ],
            ),
            C(
                msg="(name:str=<default nameue>)",
                fn=f_str__default_value,
                expected=[
                    {'name': 'add_argument', 'args': ('--name',), 'kwargs': {'required': True, "default": _DEFAULT_STR}}, # noqa
                ],
            ),
            C(
                msg="(val:int)",
                fn=f_int,
                expected=[
                    {'name': 'add_argument', 'args': ('--val',), 'kwargs': {'required': True, 'type': "<class 'int'>"}}, # noqa
                ],
            ),
            C(
                msg="(val:int=<default value>)",
                fn=f_int__default_value,
                expected=[
                    {'name': 'add_argument', 'args': ('--val',), 'kwargs': {'required': True, 'type': "<class 'int'>", "default": _DEFAULT_INT}}, # noqa
                ],
            ),
            C(
                msg="(val:float)",
                fn=f_float,
                expected=[
                    {'name': 'add_argument', 'args': ('--val',), 'kwargs': {'required': True, 'type': "<class 'float'>"}}, # noqa
                ],
            ),
            C(
                msg="(val:float=<default value>)",
                fn=f_float__default_value,
                expected=[
                    {'name': 'add_argument', 'args': ('--val',), 'kwargs': {'required': True, 'type': "<class 'float'>", "default": _DEFAULT_FLOAT}}, # noqa
                ],
            ),
            C(
                msg="(verbose:bool), must be store_true",
                fn=f_bool,
                expected=[
                    {'name': 'add_argument', 'args': ('--verbose',), 'kwargs': {'action': "store_true"}}, # noqa
                ],
            ),
            C(
                msg="(verbose:bool=True), must be store_false",
                fn=f_bool__default_is_true,
                expected=[
                    {'name': 'add_argument', 'args': ('--verbose',), 'kwargs': {'action': "store_false"}}, # noqa
                ],
            ),
        ]
        # yapf: enable
        for c in candidates:
            with self.subTest(msg=c.msg):
                try:
                    self._callFUT(c.fn, argv=[])
                except ParseArgsCalled as e:
                    got = e.history[1:-1]
                else:
                    raise self.fail("something wrong")

                got_str = json.dumps(got, indent=2, ensure_ascii=False, sort_keys=True, default=str)
                expected_str = json.dumps(
                    c.expected, indent=2, ensure_ascii=False, sort_keys=True, default=str
                )

                debug_print("got is", got_str)
                debug_print("expected is", expected_str)

                self.assertEqual(got_str, expected_str, "- is got, + is expected")


def debug_print(prefix, x):
    import sys
    import os
    if os.environ.get("DEBUG"):
        print(prefix, x, file=sys.stderr)
