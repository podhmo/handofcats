import typing as t



def psum(xs: t.List[int], *, ys: t.Optional[t.List[int]] = None):
    print(f"Σ {xs} = {sum(xs)}")
    if ys:
        print(f"Σ {xs} + Σ {ys} = {sum(xs) + sum(ys)}")


def main(argv: t.Optional[t.List[str]] = None) -> t.Any:
    import argparse

    parser = argparse.ArgumentParser(prog=psum.__name__, description=psum.__doc__, formatter_class=type('_HelpFormatter', (argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter), {}))
    parser.print_usage = parser.print_help  # type: ignore
    parser.add_argument('xs', type=int, nargs='*', help='-')
    parser.add_argument('--ys', required=False, action='append', type=int, help='-')
    args = parser.parse_args(argv)
    params = vars(args).copy()
    action = psum
    return action(**params)


if __name__ == '__main__':
    main()
