from handofcats import as_command


@as_command
def greeting(*, message: str, is_surprised: bool = False, name: str = "foo") -> None:
    """ greeting message"""
    suffix = "!" if is_surprised else ""
    print("{name}: {message}{suffix}".format(name=name, message=message, suffix=suffix))
