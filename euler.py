import numpy as np

from solver import ConservationLaw

class Euler(ConservationLaw):
    def __init__(self, eos):
        self.eos = eos

    def cons(self, rho, p, *us):
        E = self.eos.energy(1/rho, p) + sum(u**2 for u in us)/2
        return np.stack([rho, rho*E] + [rho*u for u in us])

    def  density(self, q): return q[0]
    def   energy(self, q): return q[1]/q[0]
    def velocity(self, q): return q[2:]/q[0]

    def   volume(self, q): return 1/self.density(q)
    def inenergy(self, q): return self.energy(q) - np.sum(self.velocity(q)**2, axis=0)/2

    def pressure(self, q): return self.eos.pressure(self.volume(q), self.inenergy(q))
    def soundspd(self, q): return self.eos.soundspd(self.volume(q), self.pressure(q))

    def F(self, q, d):
        v = self.velocity(q)
        D, *x = v.shape
        m = (slice(None),d) + (None,)*D

        return v[d,None]*q + self.pressure(q)*np.concatenate((
            np.broadcast_to(np.zeros(()), [1]+x),
            np.broadcast_to(v[d,None],    [1]+x),
            np.broadcast_to(np.eye(D)[m], [D]+x),
            ), axis=0)

    def smax(self, q):
        return abs(self.velocity(q)) + self.soundspd(q)

