import numpy as np

def lidx(i, D): return (slice(None),) + tuple((slice(None, -1) if j == i else slice(1,-1)) for j in range(0,D))
def ridx(i, D): return (slice(None),) + tuple((slice( 1, None) if j == i else slice(1,-1)) for j in range(0,D))

class ConservationLaw:
    def cfl(self, q, h, cfl=0.95):
        D = len(h)
        space_dims = tuple(range(-D,0))
        return cfl*np.min(h/np.max(self.smax(q), axis=space_dims))/D

    def llf(self, D, ql, qr, fl, fr, dx, dt, i, *fargs):
        lam = D*dt/dx
        return (fr + fl - (qr - ql)/lam)/2

    def force(self, D, ql, qr, fl, fr, dx, dt, i, *fargs):
        lam = D*dt/dx
        lf =        (fr + fl - (qr - ql)/lam)/2
        lw = self.F((qr + ql - (fr - fl)*lam)/2, i, *fargs)
        return (lf + lw)/2

    def update(self, q, h, dt):
        D = len(h)
        Q = np.pad(q, (((0,0),) + ((1,1),)*D), 'edge')

        def flux(i):
            F = self.F(Q, i)
            return self.force(D, Q[lidx(i,D)], Q[ridx(i,D)], F[lidx(i,D)], F[ridx(i,D)], h[i], dt, i)

        return q - dt*sum(np.diff(flux(i), axis=i+1)/h[i] for i in range(0,D))

class ModifiedConservationLaw(ConservationLaw):
    def update(self, D, h, dt, q):
        Q = np.pad(q, (((0,0),) + ((1,1),)*D), 'edge')

        def flux(i):
            uI = self.uI(Q[lidx(i,D)], Q[ridx(i,D)])
            pI = self.pI(Q[lidx(i,D)], Q[ridx(i,D)])

            F = self.F(Q, i, uI, pI)
            H = self.H(Q, i, uI, pI)

            return self.force(D, Q[lidx(i,D)], Q[ridx(i,D)], F[lidx(i,D)], F[ridx(i,D)], h[i], dt, i, uI, pI) \
                        + self.H(Q[lidx(i,D)], Q[ridx(i,D)], uI, pI)

        return q - dt*sum(np.diff(flux(i), axis=i+1)/h[i] for i in range(0,D))


