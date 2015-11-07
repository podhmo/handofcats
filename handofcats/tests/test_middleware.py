# -*- coding:utf-8 -*-
import unittest


class TestMiddlewareApplicator(unittest.TestCase):
    def _makeOne(self, middlewares):
        from handofcats.middlewares import MiddlewareApplicator
        return MiddlewareApplicator(middlewares)

    def test_application_orders(self):
        orders = []
        expected_result = object()
        expected_arg = object()

        def foo_phase(context, fn):
            orders.append(("before", "foo"))
            result = fn(context)
            self.assertEqual(result, expected_result)
            orders.append(("after", "foo"))
            return result

        def boo_phase(context, fn):
            orders.append(("before", "boo"))
            result = fn(context)
            self.assertEqual(result, expected_result)
            orders.append(("after", "boo"))
            return result

        def bar_phase(context, fn):
            orders.append(("before", "bar"))
            result = fn(context)
            self.assertEqual(result, expected_result)
            orders.append(("after", "bar"))
            return result

        applicator = self._makeOne([foo_phase, boo_phase, bar_phase])

        @applicator
        def caller_function(args):
            orders.append(("fn", "fn"))
            self.assertEqual(args, expected_arg)
            return expected_result

        caller_function(expected_arg)
        self.assertEqual(orders, [
            ("before", "foo"),
            ("before", "boo"),
            ("before", "bar"),
            ("fn", "fn"),
            ("after", "bar"),
            ("after", "boo"),
            ("after", "foo"),
        ])
