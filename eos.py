import __builtin__
np = __import__(__builtin__.np) if hasattr(__builtin__, 'np') else __import__('numpy')

class IdealGas:
    def __init__(self, gamma):
        self.gamma = gamma

    def energy(self, v, p):
        return p*v/(self.gamma - 1)
    def pressure(self, v, e):
        return e*(self.gamma - 1)/v
    def soundspd(self, v, p):
        return np.sqrt(v*p*self.gamma)
