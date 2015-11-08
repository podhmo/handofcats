# -*- coding:utf-8 -*-
import logging


def middleware_verbosity_adjustment(context, create_parser):
    """logging level adjustment with -v and -q"""
    parser = create_parser(context)
    parser.add_argument(
        '-v', '--verbose', action='count', default=0,
        help="(default option: increment logging level(default is WARNING))"
    )
    parser.add_argument(
        '-q', '--quiet', action='count', default=0,
        help="(default option: decrement logging level(default is WARNING))"
    )

    def setup_closure(args):
        logging_level = logging.WARN + 10 * args.quiet - 10 * args.verbose
        logging.basicConfig(level=logging_level)
        return args

    parser.add_callback(setup_closure)
    return parser
