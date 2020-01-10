class CatchParseArgsArgumentParser:
    def __init__(self, *args, **kwargs):
        self.history = []

    def __getattr__(self, name):
        self.history.append({"name": name})
        return self

    def __call__(self, *args, **kwargs):
        latest = self.history[-1]
        assert "args" not in latest
        latest["args"] = args
        latest["kwargs"] = kwargs

    def parse_args(self, *args, **kwargs):
        return self.history
