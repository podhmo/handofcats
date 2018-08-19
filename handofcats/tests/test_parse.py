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

        def f0(*, name: str) -> None:
            pass

        def f1(*, x: str) -> None:
            pass

        def f2(*, val: int) -> None:
            pass

        def f3(*, val: float) -> None:
            pass

        # yapf: disable
        candidates = [
            C(
                msg="(name:str), must be --name",
                fn=f0,
                expected=[
                    {'name': 'add_argument', 'args': ('--name',), 'kwargs': {'required': True}},
                ],
            ),
            C(
                msg="(x:str), short option, must be -x",
                fn=f1,
                expected=[
                    {'name': 'add_argument', 'args': ('-x',), 'kwargs': {'required': True}},
                ],
            ),
            C(
                msg="(val:int)",
                fn=f2,
                expected=[
                    {'name': 'add_argument', 'args': ('--val',), 'kwargs': {'required': True, 'type': "<class 'int'>"}}, # noqa
                ],
            ),
            C(
                msg="(val:float)",
                fn=f3,
                expected=[
                    {'name': 'add_argument', 'args': ('--val',), 'kwargs': {'required': True, 'type': "<class 'float'>"}}, # noqa
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
