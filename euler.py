import numpy as np

from solver import ConservationLaw

class Euler(ConservationLaw):
    def __init__(self, eos):
        self.eos = eos

    def cons(self, rho, p, *us):
        rho, v, p, *us = [np.asarray(x) for x in (rho, 1/rho, p) + us]
        E = self.eos.energy(v, p) + sum(u**2 for u in us)/2
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
            ))
    def S(self, q):
        return np.zeros_like(q)

    def smax(self, q):
        return abs(self.velocity(q)) + self.soundspd(q)

    def transmit(self, q, d):
        return q
    def reflect(self, q, d):
        return self.cons(self.density(q), self.pressure(q),
                *[(-v if i == d else v) for (i,v) in enumerate(self.velocity(q))])
