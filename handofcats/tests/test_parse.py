import typing as t
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
            create_parser = testing.create_parser

        return target_function(fn=fn, argv=argv, _force=True, driver=MyDriver)

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

        def f_str__default_none(*, name: str = None) -> None:
            pass

        def f_int(*, val: int) -> None:
            pass

        def f_int__default_value(*, val: int = _DEFAULT_INT) -> None:
            pass

        def f_int__default_none__optional(*, name: t.Optional[int] = None) -> None:
            pass

        def f_float(*, val: float) -> None:
            pass

        def f_float__default_value(*, val: float = _DEFAULT_FLOAT) -> None:
            pass

        def f_bool(*, verbose: bool) -> None:
            pass

        def f_bool__default_is_true(*, verbose: bool = True) -> None:
            pass

        def f_positionals(x: str, y: int, z: bool = False) -> None:
            pass

        # t.Sequence
        def f_list(*, xs: t.List[int]) -> None:
            pass

        def f_list__any(*, xs: list = None) -> None:
            pass

        def f_list__any2(*, xs: list = []) -> None:
            pass

        def f_tuple(*, xs: t.Tuple[int]) -> None:
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
                msg="(name:str=<default value>)",
                fn=f_str__default_value,
                expected=[
                    {'name': 'add_argument', 'args': ('--name',), 'kwargs': {'required': False, "default": _DEFAULT_STR, "help": "(default: {!r})".format(_DEFAULT_STR)}}, # noqa
                ],
            ),
            C(
                msg="(name:str=None",
                fn=f_str__default_none,
                expected=[
                    {'name': 'add_argument', 'args': ('--name',), 'kwargs': {'required': False}}, # noqa
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
                    {'name': 'add_argument', 'args': ('--val',), 'kwargs': {'required': False, 'type': "<class 'int'>", "default": _DEFAULT_INT, "help": "(default: {!r})".format(_DEFAULT_INT)}}, # noqa
                ],
            ),
            C(
                msg="(name:t.Optiona[int]=None",
                fn=f_int__default_none__optional,
                expected=[
                    {'name': 'add_argument', 'args': ('--name',), 'kwargs': {'required': False, "type": "<class 'int'>"}}, # noqa
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
                    {'name': 'add_argument', 'args': ('--val',), 'kwargs': {'required': False, 'type': "<class 'float'>", "default": _DEFAULT_FLOAT, "help": "(default: {!r})".format(_DEFAULT_FLOAT)}}, # noqa
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
            # positional arguments
            C(
                msg="positionals",
                fn=f_positionals,
                expected=[
                    {'name': 'add_argument', 'args': ('x',), 'kwargs': {}}, # noqa
                    {'name': 'add_argument', 'args': ('y',), 'kwargs': {'type': "<class 'int'>"}}, # noqa
                    {'name': 'add_argument', 'args': ('-z',), 'kwargs': {'action': "store_true"}}, # noqa
                ],
            ),
            # t.Sequence
            C(
                msg="(xs:t.List[int]), must be append",
                fn=f_list,
                expected=[
                    {'name': 'add_argument', 'args': ('--xs',), 'kwargs': {'action': "append", "required": True, "type": "<class 'int'>"}}, # noqa
                ],
            ),
            C(
                msg="(xs:list=None), must be append",
                fn=f_list__any,
                expected=[
                    {'name': 'add_argument', 'args': ('--xs',), 'kwargs': {'action': "append", "required": False}}, # noqa
                ],
            ),
            C(
                msg="(xs:list=[]), must be append",
                fn=f_list__any2,
                expected=[
                    {'name': 'add_argument', 'args': ('--xs',), 'kwargs': {'action': "append", "required": False}}, # noqa
                ],
            ),
            C(
                msg="(xs:t.Tuple[int]), must be append",
                fn=f_tuple,
                expected=[
                    {'name': 'add_argument', 'args': ('--xs',), 'kwargs': {'action': "append", "required": True, "type": "<class 'int'>"}}, # noqa
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
