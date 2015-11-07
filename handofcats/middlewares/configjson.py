# -*- coding:utf-8 -*-
import argparse
from cached_property import cached_property as reify

_marker = object()


class MixedArgs(object):
    def __init__(self, parser, args, defaults):
        self.parser = parser
        self.args = args
        self.defaults = defaults

    @reify
    def default_value_mapping(self):
        return {ac.dest: ac.default for ac in self.parser._actions}

    def __getattr__(self, k):
        value = getattr(self.args, k, _marker)
        default_value = self.default_value_mapping.get(k)
        if default_value != value:
            # settings by command line option
            return value
        else:
            return getattr(self.defaults, k) or default_value


class ObjectLikeDict(dict):
    __getattr__ = dict.get


class LoadJSONConfigAction(argparse.Action):
    def __call__(self, parser, namespace, val, option_string=None):
        import json

        if val.startswith("file://"):
            with open(val.lstrip("file://")) as rf:
                data = json.load(rf, object_pairs_hook=ObjectLikeDict)
        else:
            data = json.loads(val, object_pairs_hook=ObjectLikeDict)
        setattr(namespace, self.dest, data)


def middleware_config_json(context, create_parser):
    parser = create_parser(context)
    parser.add_argument("--config", action=LoadJSONConfigAction, help="(default option: configuration via json)")

    def setup_closure(args):
        if args.config is not None:
            return MixedArgs(parser, args, args.config)
    parser.action(setup_closure)
    return parser
