import numpy as np

class System:
    def cfl(self, q, h, cfl=0.95):
        D = len(h)
        return cfl*np.min(h/np.max(self.smax(q), axis=tuple(range(-D,0))))/D

    def expr(self, v):
        try:
            idx = v.index('_')
        except ValueError:
            return getattr(self, v)
        v, x = v[:idx], v[idx+1:]
        x = "xyz".find(x) if x in "xyz" else eval(x)
        return lambda q: getattr(self, v)(q)[x]
