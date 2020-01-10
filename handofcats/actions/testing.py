class ParseArgsCalled(Exception):
    def __init__(self, *, fn, history):
        self.fn = fn
        self.history = history


class CatchParseArgsArgumentParser:
    def __init__(self, *args, **kwargs):
        self.history = [{"name": "__init__", "args": args, "kwargs": kwargs}]

    def __getattr__(self, name):
        self.history.append({"name": name})
        return self

    def __call__(self, *args, **kwargs):
        latest = self.history[-1]
        assert "args" not in latest
        latest["args"] = args
        latest["kwargs"] = kwargs

    def parse_args(self, *args, **kwargs):
        raise ParseArgsCalled(fn=self.fn, history=self.history)
