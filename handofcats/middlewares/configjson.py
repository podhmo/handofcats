# -*- coding:utf-8 -*-
import argparse
import json
import sys
from cached_property import cached_property as reify
from handofcats.compat import write


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
            value = self.defaults.get(k, _marker)
            if value is _marker:
                return default_value
            else:
                return value


class ObjectLikeDict(dict):
    __getattr__ = dict.get


class LoadJSONConfigAction(argparse.Action):
    def __call__(self, parser, namespace, val, option_string=None):
        if val.startswith("file://"):
            with open(val.lstrip("file://")) as rf:
                data = json.load(rf, object_pairs_hook=ObjectLikeDict)
        else:
            data = json.loads(val, object_pairs_hook=ObjectLikeDict)
        setattr(namespace, self.dest, data)


class GenerateJSONConfigAction(argparse.Action):
    def __init__(self,
                 option_strings,
                 dest,
                 default=False,
                 required=False,
                 help=None,
                 metavar=None):
        super(GenerateJSONConfigAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=0,
            const=True,
            default=default,
            required=required,
            help=help)

    def __call__(self, parser, namespace, val, option_string=None):
        json_data = json.dumps(self.generate_dict(parser), indent=2, sort_keys=True)
        write(sys.stdout, json_data)
        parser.exit()

    DEFAULT_EXCLUDES = ("generate_cli_skeleton", "cli_input_json", "quiet", "verbose", "help")

    def generate_dict(self, parser, excludes=set(DEFAULT_EXCLUDES)):
        d = {}
        for action in parser._actions:
            name = action.dest
            if name in excludes:
                continue
            if action.default == argparse.SUPPRESS:
                d[name] = ""
            else:
                d[name] = action.default
        return d


def middleware_config_json(context, create_parser):
    parser = create_parser(context)
    parser.add_argument("--cli-input-json",
                        action=LoadJSONConfigAction,
                        help="(default option: configuration via json)")
    parser.add_argument("--generate-cli-skeleton",
                        action=GenerateJSONConfigAction,
                        help="(default option: generate skeleton for config json)")

    def setup_closure(args):
        if args.cli_input_json is not None:
            return MixedArgs(parser, args, args.cli_input_json)
    parser.add_callback(setup_closure)
    return parser
