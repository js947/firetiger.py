import numpy as np

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

    flux = force

    def update(self, q, h, dt):
        D = len(h)
        Q = np.pad(q, (((0,0),) + ((1,1),)*D), 'edge')

        def f(i, flux=self.force):
            lidx = (slice(None),) + tuple((slice(None, -1) if j == i else slice(1,-1)) for j in range(0,D))
            ridx = (slice(None),) + tuple((slice( 1, None) if j == i else slice(1,-1)) for j in range(0,D))

            F = self.F(Q, i)
            return flux(D, Q[lidx], Q[ridx], F[lidx], F[ridx], h[i], dt, i)

        return q - dt*sum(np.diff(f(i), axis=i+1)/h[i] for i in range(0,D)) + dt*self.S(q)


class ModifiedConservationLaw(ConservationLaw):
    def update(self, q, h, dt):
        D = len(h)
        Q = np.pad(q, (((0,0),)*2 + ((1,1),)*D), 'edge')

        def flux(i, flux=self.force):
            lidx = (slice(None),)*2 + tuple((slice(None, -1) if j == i else slice(1,-1)) for j in range(0,D))
            ridx = (slice(None),)*2 + tuple((slice( 1, None) if j == i else slice(1,-1)) for j in range(0,D))

            ljdx = tuple(slice(None, -1) if j == i else slice(None) for j in range(0,D))
            rjdx = tuple(slice( 1, None) if j == i else slice(None) for j in range(0,D))

            print(' q', q.shape)
            print(' Q', Q.shape, Q[lidx].shape)
            uI = self.uI(Q[lidx], Q[ridx])
            pI = self.pI(Q[lidx], Q[ridx])

            #Fl = self.F(Q, i, uI[(slice(None),)+ljdx], pI[ljdx])
            #Fr = self.F(Q, i, uI[(slice(None),)+rjdx], pI[rjdx])

            #print('Fl', Fl.shape)
            #print('Fr', Fr.shape)

            H = self.H(Q[lidx], i, uI, pI)
            print(' H', H.shape)
            return H

            #return flux(D, Q[lidx], Q[ridx], F[lidx], F[ridx], h[i], dt, i, uI, pI) \
                  #+ self.H(Q[lidx], Q[ridx], uI, pI)

        return q - dt*sum(np.diff(flux(i), axis=i+2)/h[i] for i in range(0,D))

