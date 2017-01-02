import numpy as np

from solver import ConservationLaw

class ReactiveEuler(ConservationLaw):
    def __init__(self, eos, rr, z):
        self.eos, self.rr, self.z = eos, rr, z

    def cons(self, rho, p, l, *us):
        rho, v, p, l, *us = [np.asarray(x) for x in (rho, 1/rho, p, l) + us]
        E = self.eos.energy(v, p) - self.z*l + sum(u**2 for u in us)/2
        return np.stack([rho, rho*E, rho*l] + [rho*u for u in us])

    def  density(self, q): return q[0]
    def   energy(self, q): return q[1]/q[0]
    def    lamda(self, q): return q[2]/q[0]
    def velocity(self, q): return q[3:]/q[0]

    def   volume(self, q): return 1/self.density(q)
    def inenergy(self, q): return self.energy(q) + self.z*self.lamda(q) - np.sum(self.velocity(q)**2, axis=0)/2

    def pressure(self, q): return self.eos.pressure(self.volume(q), self.inenergy(q))
    def soundspd(self, q): return self.eos.soundspd(self.volume(q), self.pressure(q))
    def temperature(self, q): return self.eos.temperature(self.volume(q), self.inenergy(q))

    def F(self, q, d):
        v = self.velocity(q)
        D, *x = v.shape
        m = (d,slice(None)) + (None,)*D

        return v[d,None]*q + self.pressure(q)*np.concatenate((
            np.broadcast_to(np.zeros(()), [1]+x),
            np.broadcast_to(v[d,None],    [1]+x),
            np.broadcast_to(np.zeros(()), [1]+x),
            np.broadcast_to(np.eye(D)[m], [D]+x),
            ))
    def S(self, q):
        x = list(q.shape[1:])
        D = len(x)
        k = self.rr(self, q)
        return np.concatenate((
            np.broadcast_to(np.zeros(()), [2]+x),
            np.broadcast_to(k[None],      [1]+x),
            np.broadcast_to(np.zeros(()), [D]+x),
            ))

    def smax(self, q):
        return abs(self.velocity(q)) + self.soundspd(q)

    def transmit(self, q, d):
        return q
    def reflect(self, q, d):
        return self.cons(self.density(q), self.pressure(q), self.lamda(q),
                *[(-v if i == d else v) for (i,v) in enumerate(self.velocity(q))])
