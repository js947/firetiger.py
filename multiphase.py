import numpy as np

from solver import ModifiedConservationLaw

class Multiphase(ModifiedConservationLaw):
    def __init__(self, *eos):
        self.eos = eos

    def cons(self, alpha, rho, p, *us):
        alpha = np.asarray(alpha)
        rho = np.asarray(rho)
        p = np.asarray(p)
        us = [np.asarray(u) for u in us]

        E = np.stack(
            eos.energy(1/rho[i], p[i]) + sum(u[i]**2 for u in us)/2
            for i, eos in enumerate(self.eos))
        return np.stack([alpha, alpha*rho, alpha*rho*E] + [alpha*rho*u for u in us])

    def    alpha(self, q): return q[0]
    def  density(self, q): return q[1]/q[0]
    def   energy(self, q): return q[2]/q[1]
    def velocity(self, q): return q[3:]/q[1]

    def volume(self, q):
        return 1 / self.density(q)
    def lamda(self, q):
        return self.alpha(q)*self.density(q)/self.mdensity(q)
    def inenergy(self, q):
        return self.energy(q) - np.sum(self.velocity(q)**2, axis=0)/2

    def pressure(self, q):
        v = self.volume(q)
        e = self.inenergy(q)
        return np.stack(eos.pressure(v[i], e[i]) for i, eos in enumerate(self.eos))
    def soundspd(self, q):
        v = self.volume(q)
        p = self.pressure(q)
        return np.stack(eos.soundspd(v[i], p[i]) for i, eos in enumerate(self.eos))

    def mdensity(self, q):
        return np.sum(self.alpha(q)*self.density(q), axis=0)

    def uI(self, ql, qr): return (self.mvelocity(ql) + self.mvelocity(qr))/2
    def pI(self, ql, qr): return (self.mpressure(ql) + self.mpressure(qr))/2
    def smax(self, q):
        return np.max(abs(self.velocity(q)) + self.soundspd(q), axis=1)
    # def F(self, q, pI, uI):
    #     a = self.alpha(q)
    #     v = self.velocity(q)
    #     p = self.pressure(q)
    #     D, *x = v.shape

    #     d0 = np.broadcast_to(np.zeros(1), (D,)+v.shape)
    #     d1 = np.concatenate((
    #         np.broadcast_to(np.zeros(1),                                 (D,) +v.shape),
    #         np.broadcast_to(np.zeros(D)[(slice(None),None) + (None,)*D], (D,2)+v.shape[1:]),
    #         np.broadcast_to(v[:,None],                                   (D,1)+v.shape[1:]),
    #         np.broadcast_to(np.eye(D)[(slice(None),)*2 + (None,)*D],     (D,D)+v.shape[1:]),
    #         ), axis=1)
    #     d2 = np.concatenate((
    #         np.broadcast_to(np.zeros(1),                                 (D,) +v.shape),
    #         np.broadcast_to(np.zeros(D)[(slice(None),None) + (None,)*D], (D,2)+v.shape[1:]),
    #         np.broadcast_to(vI[:,None],                                  (D,1)+v.shape[1:]),
    #         np.broadcast_to(np.eye(D)[(slice(None),)*2 + (None,)*D],     (D,D)+v.shape[1:]),
    #         ), axis=1)
    #     d3 = self.alpha(q)*np.concatenate((
    #         np.broadcast_to(vI[:,None],  (D,))
    #         np.broadcast_to(np.zeros(1), ())
    #         ), axis=1)

    #     return v[:,None]*q*d0 + a*p*d1 - a*pI*d2 + a*d3

