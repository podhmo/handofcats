import typing as t
import typing_extensions as tx
import sys
import warnings
import itertools
from logging import getLogger as get_logger
from .langhelpers import reify
from .accessor import Accessor

logger = get_logger(__name__)

if sys.version_info[:2] <= (3, 6):

    def _has_origin(typ) -> bool:
        return (hasattr(typ, "__origin__") and hasattr(typ, "__args__")) or _is_literal(
            typ
        )

    def _is_literal(typ) -> bool:
        return str(type(typ)) == "typing_extensions.Literal"


else:

    def _has_origin(typ) -> bool:
        return hasattr(typ, "__origin__") and hasattr(typ, "__args__")

    def _is_literal(typ) -> bool:
        return getattr(typ, "__origin__", None) == tx.Literal


class Injector:
    """inject arguments to argparse.ArgumentParser from function definition"""

    def __init__(self, fn):
        self.fn = fn

    @reify
    def accessor(self):
        return Accessor(self.fn)

    def _handle_type(self, opt, kwargs, *, _nonetype=type(None)):
        if opt.type == bool:
            action = "store_true"
            if opt.default is True:
                action = "store_false"
            kwargs.pop("required", None)
            kwargs.pop("default", None)
            kwargs["action"] = action
        elif opt.type in (int, float):
            kwargs["type"] = opt.type
        else:
            from collections.abc import Sequence

            if _has_origin(opt.type):
                try:
                    # for Optional
                    if (
                        opt.type.__origin__ == t.Union
                        and _nonetype in opt.type.__args__
                        and len(opt.type.__args__) == 2
                    ):
                        item_type = opt._replace(
                            type=[t for t in opt.type.__args__ if t is not _nonetype][0]
                        )
                        kwargs["required"] = False
                        self._handle_type(item_type, kwargs)

                    # for Literal type (e.g. tx.Literal["r", "g", "b"])
                    if _is_literal(opt.type):
                        kwargs["choices"] = list(opt.type.__args__)
                        item_type = opt._replace(type=type(opt.type.__args__[0]))
                        self._handle_type(item_type, kwargs)
                    # for sequence (e.g. t.List[int], t.Tuple[str])
                    elif issubclass(opt.type.__origin__, Sequence):
                        kwargs["action"] = "append"
                        item_type = opt._replace(type=opt.type.__args__[0])
                        self._handle_type(item_type, kwargs)
                except Exception:  # TODO: remove this
                    logger.info(
                        "unexpected generic type is found (type=%s)",
                        opt.type,
                        exc_info=True,
                    )
            elif hasattr(opt.type, "__supertype__"):  # for NewType
                # choices support (tentative)
                if hasattr(opt.type, "choices"):
                    warnings.warn(
                        "choices is deprecated, use typing_extensions.Literal instead of this"
                    )
                    kwargs["choices"] = opt.type.choices
                origin_type = opt._replace(type=opt.type.__supertype__)
                self._handle_type(origin_type, kwargs)
            elif issubclass(opt.type, (list, tuple)):
                kwargs["action"] = "append"
            else:
                logger.info("unexpected type is found (type=%s)", opt.type)

    def inject(
        self,
        parser,
        *,
        ignore_arguments: bool = False,
        ignore_flags: bool = False,
        help_default: t.Optional[
            t.Union[str, t.Callable[[t.Dict[str, t.Any]], None]]
        ] = "-",  # need by argparse.ArgumentDefaultsHelpFormatter
        callback: t.Callable[[t.Any], t.Any] = id,
    ):
        arguments = [(opt, None) for opt in self.accessor.arguments]
        flags = [(opt, opt.required) for opt in self.accessor.flags]
        if ignore_arguments:
            arguments = []
        if ignore_flags:
            flags = []

        for opt, required in itertools.chain(arguments, flags):
            kwargs = {}
            if required is not None:
                kwargs["required"] = required
            if opt.default is not None:
                kwargs["default"] = opt.default
            if opt.type and opt.type != str:
                self._handle_type(opt, kwargs)
            if kwargs.get("action") == "append" and not opt.option_name.startswith("-"):
                kwargs["nargs"] = "*"
                kwargs.pop("action")

            if help_default is not None:
                if callable(help_default):
                    help_default(kwargs)
                else:
                    kwargs["help"] = help_default

            logger.debug("add_argument %s %r", opt.option_name, kwargs)
            callback(parser.add_argument(opt.option_name, **kwargs))


def _help_default(kwargs: t.Dict[str, t.Any]):
    """
    append help message generated from default value

    NOTE: if using argparse.ArgumentDefaultsHelpFormatter, this is default behaviour.
    """
    if "default" in kwargs:
        kwargs["help"] = "(default: {!r})".format(kwargs["default"])
