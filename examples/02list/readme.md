help
```console
handofcats sum.py:psum -h
usage: handofcats [-h] [--expose] [--ys YS] [xs [xs ...]]

positional arguments:
  xs

optional arguments:
  -h, --help  show this help message and exit
  --expose
  --ys YS
```
run
```console
handofcats sum.py:psum 10 20
Σ [10, 20] = 30
handofcats sum.py:psum 10 20 --ys 1 --ys 2
Σ [10, 20] = 30
Σ [10, 20] + Σ [1, 2] = 33
```
