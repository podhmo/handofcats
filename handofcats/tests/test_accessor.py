import unittest


class Tests(unittest.TestCase):
    def _makeOne(self, fn):
        from handofcats.accessor import Accessor
        return Accessor(fn)

    def test_args(self):
        def f(user_name: str) -> None:
            pass

        target = self._makeOne(f)
        with self.subTest("arguments"):
            got = target.arguments
            self.assertEqual(len(got), 1)

            with self.subTest("option_name"):
                self.assertEqual(got[0].option_name, "user_name")
            with self.subTest("required"):
                self.assertEqual(got[0].required, True)
            with self.subTest("default"):
                self.assertEqual(got[0].default, None)

        with self.subTest("flags"):
            got = target.flags
            self.assertEqual(len(got), 0)

    def test_kwonlyargs(self):
        def f(*, user_name: str) -> None:
            pass

        target = self._makeOne(f)
        with self.subTest("arguments"):
            got = target.arguments
            self.assertEqual(len(got), 0)

        with self.subTest("flags"):
            got = target.flags
            self.assertEqual(len(got), 1)

            with self.subTest("option_name"):
                self.assertEqual(got[0].option_name, "--user-name")
            with self.subTest("required"):
                self.assertEqual(got[0].required, True)
            with self.subTest("default"):
                self.assertEqual(got[0].default, None)

    def test_kwonlyargs_with_type_bool(self):
        def f(*, verbose: bool) -> None:
            pass

        target = self._makeOne(f)
        with self.subTest("flags"):
            got = target.flags
            self.assertEqual(len(got), 1)

            with self.subTest("type"):

                self.assertEqual(got[0].type, bool)

    def test_kwonlyargs_with_type_int(self):
        def f(*, val: int) -> None:
            pass

        target = self._makeOne(f)
        with self.subTest("flags"):
            got = target.flags
            self.assertEqual(len(got), 1)

            with self.subTest("type"):
                self.assertEqual(got[0].type, int)

            with self.subTest("required"):
                self.assertEqual(got[0].required, True)


if __name__ == "__main__":
    unittest.main()
