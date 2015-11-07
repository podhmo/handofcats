# -*- coding:utf-8 -*-
from handofcats import as_command
import logging
logger = logging.getLogger(__name__)


@as_command
def greeting(message, is_surprised=False, name="foo"):
    """ greeting message

    :param message: message of greeting
    :param is_surprised: surprised or not (default=False)
    :param name: name of actor
    """
    logger.info("greeting start (name=%s)", name)
    suffix = "!" if is_surprised else ""
    print("{name}: {message}{suffix}".format(name=name, message=message, suffix=suffix))
