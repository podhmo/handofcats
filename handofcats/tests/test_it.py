import unittest
import contextlib
from functools import partial


@contextlib.contextmanager
def check_status(testcase, *, status):
    called = [False]

    def activate():
        called[0] = True

    yield activate
    testcase.assertEqual(called[0], status)


mustcall = partial(check_status, status=True)
mustnotcall = partial(check_status, status=False)


class Tests(unittest.TestCase):
    def _callFUT(self, fn, *, argv):
        from handofcats import as_command as target_function
        return target_function(fn=fn, argv=argv, force=True)

    def test_it(self):
        with mustcall(self) as mark:

            def f(*, name: str):
                self.assertEqual(name, "foo")
                mark()

            self._callFUT(f, argv=["--name", "foo"])

    # todo: boolean, float, int
