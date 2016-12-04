import __builtin__
np = __import__(__builtin__.np) if hasattr(__builtin__, 'np') else __import__('numpy')

class Euler:
    def __init__(self, eos):
        self.eos = eos

    def cons(self, rho, p, *us):
        E = self.eos.energy(1/rho, p) + np.sqrt(sum(u**2 for u in us))
        return np.stack([rho, rho*E] + [rho*u for u in us])

    def  density(self, q): return q[0]
    def   energy(self, q): return q[1]/q[0]
    def velocity(self, q): return q[2:]/q[0]

    def volume(self, q):
        return 1 / self.density(q)
    def inenergy(self, q):
        return self.energy(q) - np.sqrt(np.sum(self.velocity(q)*self.velocity(q), axis=0))

    def pressure(self, q):
        return self.eos.pressure(self.volume(q), self.inenergy(q))
    def soundspd(self, q):
        return self.eos.soundspd(self.volume(q), self.pressure(q))

    def smax(self, q):
        return abs(self.velocity(q)) + self.soundspd(q)
    def F(self, q):
        v = self.velocity(q)
        D = v.shape[0]

        z_idx = (slice(None),None) + (None,)*D
        e_idx = (slice(None),)*2 + (None,)*D

        return v[:,None]*q + self.pressure(q)*np.concatenate((
            np.broadcast_to(np.zeros(D)[z_idx], (D,1)+v.shape[1:]),
            np.broadcast_to(v[:,None], (D,1)+v.shape[1:]),
            np.broadcast_to(np.eye(D)[e_idx], (D,D)+v.shape[1:])),
            axis=1)
