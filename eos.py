import numpy as np

class IdealGas:
    def __init__(self, gamma):
        self.gamma = gamma

    def energy(self, v, p):
        return p*v/(self.gamma - 1)
    def pressure(self, v, e):
        return e*(self.gamma - 1)/v
    def soundspd(self, v, p):
        return np.sqrt(v*p*self.gamma)
