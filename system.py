import numpy as np

class System:
    def expr(self, v):
        try:
            idx = v.index('_')
        except ValueError:
            return getattr(self, v)
        v, x = v[:idx], v[idx+1:]
        x = "xyz".find(x) if x in "xyz" else eval(x)
        return lambda q: getattr(self, v)(q)[x]
