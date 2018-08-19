import typing as t


def psum(xs: t.List[int], *, ys: t.List[int] = None):
    print(f"Σ {xs} = {sum(xs)}")
    if ys:
        print(f"Σ {xs} + Σ {ys} = {sum(xs) + sum(ys)}")
