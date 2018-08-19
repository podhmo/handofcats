import typing as t


def psum(xs: t.List[int], *, ys: t.List[int] = None):
    print(f"Σ {xs} = {sum(xs)}")
    if ys:
        print(f"Σ {xs} + Σ {ys} = {sum(xs) + sum(ys)}")

def main(argv=None):
    import argparse
    parser = argparse.ArgumentParser(description=None)
    parser.print_usage = parser.print_help
    parser.add_argument('xs', nargs='*', type=int)
    parser.add_argument('--ys', action='append', required=False, type=int)
    args = parser.parse_args(argv)
    psum(**vars(args))


if __name__ == '__main__':
    main()
