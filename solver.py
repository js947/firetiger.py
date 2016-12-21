import numpy as np

class ConservationLaw:
    def cfl(self, q, h, cfl=0.95):
        D = len(h)
        space_dims = tuple(range(-D,0))
        return cfl*np.min(h/np.max(self.smax(q), axis=space_dims))/D

    def update(self, q, h, dt):
        D = len(h)
        Q = np.pad(q, (((0,0),) + ((1,1),)*D), 'edge')
        F = self.F(Q)

        def flux(i):
            lidx = (slice(None),) + tuple((slice(None, -1) if j == i else slice(1,-1)) for j in range(0,D))
            ridx = (slice(None),) + tuple((slice( 1, None) if j == i else slice(1,-1)) for j in range(0,D))

            return self.force(D, Q[lidx], Q[ridx], F[(i,)+lidx], F[(i,)+ridx], h[i], dt, i)

        return q - dt*sum(np.diff(flux(i), axis=i+1)/h[i] for i in range(0,D))

    def llf(sys, D, ql, qr, fl, fr, dx, dt):
        lam = D*dt/dx
        return (fr + fl - (qr - ql)/lam)/2

    def force(sys, D, ql, qr, fl, fr, dx, dt, i):
        lam = D*dt/dx
        lf =       (fr + fl - (qr - ql)/lam)/2
        lw = sys.F((qr + ql - (fr - fl)*lam)/2)[i]
        return (lf + lw)/2


class ModifiedConservationLaw(ConservationLaw):
    def update(self, D, h, dt, q):
        Q = np.pad(q, (((0,0),) + ((1,1),)*D), 'edge')
        F = sys.F(Q)
        H = sys.H(Q)

        def flux(i):
            lidx = (slice(None),) + tuple((slice(None, -1) if j == i else slice(1,-1)) for j in range(0,D))
            ridx = (slice(None),) + tuple((slice( 1, None) if j == i else slice(1,-1)) for j in range(0,D))

            return force(D, sys, Q[lidx], Q[ridx], F[(i,)+lidx], F[(i,)+ridx], h[i], dt, i)

        return q - dt*sum(np.diff(flux(i), axis=i+1)/h[i] for i in range(0,D))


