#!/usr/bin/env python3
import pickle
import argparse
import numpy as np
import h5py

from eos import IdealGas
from euler import Euler

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-x", help="x resolution", default=1000, type=int)
parser.add_argument("-y", help="y resolution", default= 600, type=int)
args = parser.parse_args()

sys = Euler(IdealGas(1.4))

def coord(x0, x1, nx):
    x, dx = np.linspace(x0, x1, nx+1, retstep=True)
    x += dx/2
    return x[:-1], dx

x, dx = coord( 0.0, 3.0, args.x)
y, dy = coord(-0.9, 0.9, args.y)
x = np.meshgrid(x, y)

bubble = sys.cons(0.1, 1.0, 0.0, 0.0)
shock  = sys.cons(3.81062, 9.98625, 0.0, 2.5745)
amb    = sys.cons(1.0, 1.0, 0.0, 0.0)

m = (slice(None),) + (None,)*2
is_shock  = x[0] < 0.05
is_bubble = np.sqrt(sum((x - np.array([0.5, 0.0])[m])**2)) < 0.35
q = np.where(is_bubble, bubble[m], np.where(is_shock, shock[m], amb[m]))

f = h5py.File('bubble.h5', 'w')
f.attrs['system'] = np.string_(pickle.dumps(sys))
h_ = f.create_dataset('h', data=[dx, dy])
x_ = f.create_dataset('x', data=x)

i_ = f.create_dataset('i', (1,), maxshape=(None,), dtype='i')
t_ = f.create_dataset('t', (1,), maxshape=(None,), dtype='f')
q_ = f.create_dataset('q', (1,)+q.shape, maxshape=(None,)+q.shape, dtype='f', compression="lzf")

t_[0] = 0.0
i_[0] = 0
q_[0] = q
