#!/usr/bin/env python3
import pickle
import argparse
import numpy as np
import h5py

from eos import IdealGas
from euler import Euler

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-x", help="x resolution", default=200, type=int)
parser.add_argument("-c", help="test case", default=1, type=int)
parser.add_argument("-o", help="simulation file", default="shock-tube.h5", type=str)
parser.add_argument("-D", help="dimensions",default=1, type=int)
parser.add_argument("-d", help="dimension in which to make the shock", default='x', choices='xyz', type=str)
args = parser.parse_args()

sys = Euler(IdealGas(1.4))

def coord(x0, x1, nx):
    x, dx = np.linspace(x0, x1, nx+1, retstep=True)
    x += dx/2
    return x[:-1], dx

def vd(v):
    return [v if i == args.d else 0.0 for i in range(0,args.D)]

m, qL, qR = {
    0: (0.3, sys.cons(    1.0,     1.0, *vd(     0.0)), sys.cons(  0.125,    0.1, *vd(      0.0))),
    1: (0.3, sys.cons(    1.0,     1.0, *vd(    0.75)), sys.cons(  0.125,    0.1, *vd(      0.0))),
    2: (0.5, sys.cons(    1.0,     0.4, *vd(    -2.0)), sys.cons(    1.0,    0.4, *vd(      2.0))),
    3: (0.5, sys.cons(    1.0,  1000.0, *vd(     0.0)), sys.cons(    1.0,   0.01, *vd(      0.0))),
    4: (0.3, sys.cons(5.99924, 460.894, *vd( 19.5975)), sys.cons(5.99242, 46.095, *vd( -6.19633))),
    5: (0.8, sys.cons(    1.0,  1000.0, *vd(-19.5975)), sys.cons(    1.0,   0.01, *vd(-19.59745))),
}[args.c]

xdx = [coord(0.0, 1.0, args.x) for i in range(0,args.D)]
x = np.meshgrid(*[j[0] for j in xdx])

idx = (slice(None),) + (None,)*args.D
q = np.where(x[{'x':0, 'y':1, 'z':2}[args.d]] < m, qL[idx], qR[idx])

f = h5py.File(args.o, 'w')
f.attrs['system'] = np.string_(pickle.dumps(sys))

h_ = f.create_dataset('h', data=[j[1] for j in xdx])
for n, d in zip('xyz', x):
    f.create_dataset(n, data=d)

i_ = f.create_dataset('i', (1,), maxshape=(None,), dtype='i')
t_ = f.create_dataset('t', (1,), maxshape=(None,), dtype='f')
q_ = f.create_dataset('q', (1,)+q.shape, maxshape=(None,)+q.shape, dtype='f', compression="lzf")

i_[0] = 0
t_[0] = 0.0
q_[0] = q
