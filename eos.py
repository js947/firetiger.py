import numpy as np

class IdealGas:
    def __init__(self, gamma, cv=1, q=0):
        self.gamma, self.cv, self.q = gamma, cv, q

    def energy(self, v, p):
        return p*v/(self.gamma - 1) + self.q
    def pressure(self, v, e):
        return (e - self.q)*(self.gamma - 1)/v
    def soundspd(self, v, p):
        return np.sqrt(v*p*self.gamma)
    def temperature(self, v, e):
        return (e - self.q)/cv

class StiffenedGas:
    def __init__(self, gamma, p0, cv=1, q=0):
        self.gamma, self.p0, self.cv, self.q = gamma, p0, cv, q

    def energy(self, v, p):
        return (p + self.gamma*self.p0)*v/(self.gamma - 1)
    def pressure(self, v, e):
        return e*(self.gamma - 1.0)/v - self.gamma*self.p0
    def soundspd(self, v, p):
        return np.sqrt(v*(p + self.p0)*self.gamma)
    def temperature(self, v, e):
        return (e - self.q)/cv

class Arrhenius:
    def __init__(self, z, e):
        self.z, self.e = z, e

    def __call__(sys, q):
        l = np.clip(sys.lamda(q), 0, 1)
        T = sys.temperature(q)
        return (1 - l)*self.z*np.exp(-self.e/T)
