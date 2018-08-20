

def greeting(message: str, is_surprised: bool = False, name: str = "foo") -> None:
    """greeting message"""
    suffix = "!" if is_surprised else ""
    print("{name}: {message}{suffix}".format(name=name, message=message, suffix=suffix))

def main(argv=None):
    import argparse
    parser = argparse.ArgumentParser(description='greeting message')
    parser.print_usage = parser.print_help
    parser.add_argument('message')
    parser.add_argument('--is-surprised', action='store_true')
    parser.add_argument('--name', default='foo', help="(default: 'foo')", required=False)
    args = parser.parse_args(argv)
    greeting(**vars(args))


if __name__ == '__main__':
    main()
