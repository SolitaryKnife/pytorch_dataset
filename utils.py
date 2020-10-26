def eprint(*args, **kwds):
    from sys import stderr
    print(*args, file=stderr, **kwds)


def glob(pathname, *, recursive=False, key=None, reverse=False, unique=True):
    from glob import glob as _glob

    # If simple string
    if isinstance(pathname, str):
        return sorted(_glob(pathname, recursive=recursive), key=key, reverse=reverse)

    # Assume pathname is iterable
    assert all([isinstance(p, str) for p in pathname]), "pathname must be a string or string[]"

    values = []
    for path in pathname:
        values += _glob(path, recursive=recursive)

    if unique:
        from collections import OrderedDict
        values = OrderedDict.fromkeys(values).keys()

    return sorted(values, key=key, reverse=reverse)


def fill(*args, **kwds):
    paths, *args = args
    if isinstance(paths, str):
        paths = [paths]

    keys = []
    vals = []

    for val in args:
        if val is None:
            val = [""]
        if not isinstance(val, (list, tuple)):
            val = [val]
        if len(val) == 0:
            val = [""]
        vals.append(val)

    for key, val in kwds.items():
        if val is None:
            val = [""]
        if not isinstance(val, (list, tuple)):
            val = [val]
        if len(val) == 0:
            val = [""]
        keys.append(key)
        vals.append(val)

    from itertools import product
    combinations = list(product(*vals))

    out = []
    for path in paths:
        for combination in combinations:
            split = len(args)
            var_args = combination[:split]
            var_kwds = {k: v for k, v in zip(keys, combination[split:])}

            p = path.format(*var_args, **var_kwds)
            out.append(p)

    return out