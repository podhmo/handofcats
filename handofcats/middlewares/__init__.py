# -*- coding:utf-8 -*-
from functools import wraps


class MiddlewareApplicator(object):
    def __init__(self, fns):
        self.middlewares = [middlewarefy(fn) for fn in fns]

    def register(self, fn):
        self.middlewares.append(middlewarefy(fn))

    def __call__(self, fn):
        def call(*args, **kwargs):
            context = {}
            context["_args"] = args
            context["_keys"] = list(kwargs.keys())
            context.update(kwargs)

            def create_result(context):
                args = context["_args"]
                kwargs = {k: context[k] for k in context["_keys"]}
                return fn(*args, **kwargs)

            closure = create_result
            for m in reversed(self.middlewares):
                closure = m(closure)
            return closure(context)
        return call


def middlewarefy(fn):
    @wraps(fn)
    def middleware(closure):
        return lambda context: fn(context, closure)
    return middleware


def middleware_verbosity_adjustment(context, create_parser):
    """logging level adjustment with -v and -q"""
    import logging
    parser = create_parser(context)
    parser.add_argument(
        '-v', '--verbose', action='count', default=0,
        help="increment logging level(default is WARNING)"
    )
    parser.add_argument(
        '-q', '--quiet', action='count', default=0,
        help="decrement logging level(default is WARNING)"
    )

    def setup_closure(args):
        logging_level = logging.WARN + 10 * args.quiet - 10 * args.verbose
        logging.basicConfig(level=logging_level)

    parser.action(setup_closure)
    return parser


DEFAULT_MIDDLEWARES = [
    middleware_verbosity_adjustment
]
