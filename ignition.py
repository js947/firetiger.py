#!/usr/bin/env python3
import pickle
import argparse
import numpy as np
import h5py

from eos import IdealGas, Arrhenius
from reactive_euler import ReactiveEuler

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-x", help="x resolution", default=2000, type=int)
parser.add_argument("-c", help="test case", default=1, type=int)
parser.add_argument("-o", help="simulation file", default="ignition.h5", type=str)
args = parser.parse_args()

sys = ReactiveEuler(IdealGas(1.4, 0.72e3), Arrhenius(2e8, 11627.655), 2e6)
sys.x0 = sys.reflect

def coord(x0, x1, nx):
    x, dx = np.linspace(x0, x1, nx+1, retstep=True)
    x += dx/2
    return x[:-1], dx

x, dx = coord(0.0, 1.0, args.x)
q = sys.cons(1.2, 101325.0, 0.0, -775.0)

q = np.broadcast_to(q[:,None], q.shape + x.shape)

f = h5py.File(args.o, 'w')
f.attrs['system'] = np.string_(pickle.dumps(sys))

h_ = f.create_dataset('h', data=[dx])
x_ = f.create_dataset('x', data=x[None,:])

i_ = f.create_dataset('i', (1,), maxshape=(None,), dtype='i')
t_ = f.create_dataset('t', (1,), maxshape=(None,), dtype='f4')
q_ = f.create_dataset('q', (1,)+q.shape, maxshape=(None,)+q.shape, dtype='f4', compression="lzf")

i_[0] = 0
t_[0] = 0.0
q_[0] = q
