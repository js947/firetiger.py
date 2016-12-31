import numpy as np

from eos import IdealGas
from euler import Euler

eos = IdealGas(1.4)
sys = Euler(eos)

def d1():
    rho, p, vx, vy = 1.0, 1.0, 1.0, 0.0
    q = sys.cons(rho, p, vx, vy)

    assert(rho == sys.density(q))
    assert(  p == sys.pressure(q))
    assert( vx == sys.velocity(q)[0])
    assert( vy == sys.velocity(q)[1])

    assert( vx == sys.expr('velocity_x')(q) )
    assert( vy == sys.expr('velocity_y')(q) )

def d2(n):
    rho = np.ones(n)
    p   = np.ones(n)
    vx  = np.ones(n)
    vy  = np.zeros(n)
    q = sys.cons(rho, p, vx, vy)

    assert((rho == sys.density(q)).all())
    assert((  p == sys.pressure(q)).all())
    assert(( vx == sys.velocity(q)[0]).all())
    assert(( vy == sys.velocity(q)[1]).all())

    assert(( vx == sys.expr('velocity_x')(q) ).all())
    assert(( vy == sys.expr('velocity_y')(q) ).all())

d1()
d2((30))
d2((30,30))

def d3(n):
    rho = np.ones(n)
    p   = np.ones(n)
    vx  = np.ones(n)
    vy  = np.zeros(n)
    q = sys.cons(rho, p, vx, vy)

    f = h5py.File('test.h5', 'w')
    q_ = f.create_dataset('q', (1,)+q.shape, maxshape=(None,)+q.shape, dtype='f', compression="lzf")

    q_[0] = q
    f.close()

    g = h5py.File('test.h5', 'r')
    w = g['q'][0]
    assert(w == q)

    assert((rho == sys.density(w)).all())
    assert((  p == sys.pressure(w)).all())
    assert(( vx == sys.velocity(w)[0]).all())
    assert(( vy == sys.velocity(w)[1]).all())

    assert(( vx == sys.expr('velocity_x')(w) ).all())
    assert(( vy == sys.expr('velocity_y')(w) ).all())

