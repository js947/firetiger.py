import numpy as np

from solver import ModifiedConservationLaw

class Multiphase(ModifiedConservationLaw):
    def __init__(self, *eos):
        self.eos = eos

    def cons(self, alpha, rho, p, *us):
        alpha, rho, p, *us = [np.asarray(x) for x in (alpha, rho, p) + us]

        E = np.stack( eos.energy(1/rho[i], p[i]) + sum(u[i]**2 for u in us)/2
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
        v, e = self.volume(q), self.inenergy(q)
        return np.stack(eos.pressure(v[i], e[i]) for i, eos in enumerate(self.eos))
    def soundspd(self, q):
        v, p = self.volume(q), self.pressure(q)
        return np.stack(eos.soundspd(v[i], p[i]) for i, eos in enumerate(self.eos))

    def mdensity(self, q):
        return np.sum(self.alpha(q)*self.density(q), axis=0)
    def mvelocity(self, q):
        return np.sum(self.lamda(q)*self.velocity(q), axis=0)/np.sum(self.lamda(q), axis=0)
    def mpressure(self, q):
        return np.sum(self.lamda(q)*self.pressure(q), axis=0)/np.sum(self.lamda(q), axis=0)

    def uI(self, ql, qr): return (self.mvelocity(ql) + self.mvelocity(qr))/2
    def pI(self, ql, qr): return (self.mpressure(ql) + self.mpressure(qr))/2

    def F(self, q, d, uI, pI):
        a = self.alpha(q)
        v = self.velocity(q)
        p = self.pressure(q)
        D, M, *x = v.shape
        m = (slice(None),d) + (None,)*(D+1)
        m0 = (slice(None),)*2 + (None,)*D

        d0 = np.broadcast_to(np.concatenate((np.zeros(1), np.ones(2+D)))[:,None], [3+D,M])
        d1 = np.concatenate((
            np.broadcast_to(np.zeros(()), [2,M]+x),
            np.broadcast_to(v[d,None],    [1,M]+x),
            np.broadcast_to(np.eye(D)[m], [D,M]+x),
            ))
        d2 = np.concatenate((
            np.broadcast_to(np.zeros(()), [2,M]+x),
            np.broadcast_to(uI[d,None],   [1,M]+x),
            np.broadcast_to(np.eye(D)[m], [D,M]+x),
            ))
        d3 = self.alpha(q)*np.concatenate((
            np.broadcast_to(uI[d,None],   [1,M]+x),
            np.broadcast_to(np.zeros(()), [2+D,M]+x),
            ))
        return v[d,:]*q*d0[m0] + a*p*d1 - a*pI*d2 + a*d3

    def H(self, q, d, uI, pI):
        a = self.alpha(q)
        M, *x = a.shape
        D = len(x)
        return np.concatenate((
            (a*(-uI))[None,:],
            np.broadcast_to(np.zeros(()), [1,M]+x),
            (a*pI*uI)[None,:],
            (a*pI*np.broadcast_to(np.eye(D)[(slice(None),d)+(None,)*D], [D,M]+x)),
            ))

    def smax(self, q):
        return np.max(abs(self.velocity(q)) + self.soundspd(q), axis=1)
