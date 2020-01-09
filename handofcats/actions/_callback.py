class CallbackArgumentParser:
    def __init__(self, callback, fn, *args, history=None, **kwargs):
        self.callback = callback
        self.fn = fn
        self.history = history or [{"name": "__init__", "args": args, "kwargs": kwargs}]

    def __getattr__(self, name):
        self.history.append({"name": name})
        return self

    def __call__(self, *args, **kwargs):
        latest = self.history[-1]
        assert "args" not in latest
        latest["args"] = args
        latest["kwargs"] = kwargs

    def parse_args(self, *args, **kwargs):
        self.history.append({"name": "parse_args", "args": args, "kwargs": kwargs})
        self.callback(fn=self.fn, history=self.history)
