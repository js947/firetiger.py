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

    def __repr__(self):
        return "eos.IdealGas(%f)" % self.gamma

class StiffenedGas:
    def __init__(self, gamma, p0):
        self.gamma, self.p0 = gamma, p0

    def energy(self, v, p):
        return (p + self.gamma*self.p0)*v/(self.gamma - 1)
    def pressure(self, v, e):
        return e*(self.gamma - 1.0)/v - self.gamma*self.p0
    def soundspd(self, v, p):
        return np.sqrt(v*(p + self.p0)*self.gamma)

    def __repr__(self):
        return "eos.StiffenedGas(%f,%f)" % (self.gamma, self.p0)
