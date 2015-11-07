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


from .verbosity_adjustment import middleware_verbosity_adjustment
DEFAULT_MIDDLEWARES = [
    middleware_verbosity_adjustment,
]
