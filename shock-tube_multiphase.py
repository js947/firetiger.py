#!/usr/bin/env python3
import pickle
import argparse
import numpy as np
import h5py

from eos import IdealGas, StiffenedGas
from multiphase import Multiphase

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-x", help="x resolution", default=200, type=int)
parser.add_argument("-o", help="simulation file", default="shock-tube_multiphase.h5", type=str)
args = parser.parse_args()

sys = Multiphase(StiffenedGas(4.4, 6e8), IdealGas(1.4))

def coord(x0, x1, nx):
    x, dx = np.linspace(x0, x1, nx+1, retstep=True)
    x += dx/2
    return x[:-1], dx

x, dx = coord(0.0, 1.0, args.x)

rho_l, rho_g = 1000.0, 50.0
pl, pr = 1e9, 1e5
qL = sys.cons((0.5, 0.5), (rho_l, rho_g), (pl, pl), (0.0, 0.0))
qR = sys.cons((0.5, 0.5), (rho_l, rho_g), (pr, pr), (0.0, 0.0))

q = np.where(x < 0.55, qL[:,:,None], qR[:,:,None])

f = h5py.File(args.o, 'w')
f.attrs['system'] = np.string_(pickle.dumps(sys))
h_ = f.create_dataset('h', data=[dx])
x_ = f.create_dataset('x', data=x);

i_ = f.create_dataset('i', (1,), maxshape=(None,), dtype='i')
t_ = f.create_dataset('t', (1,), maxshape=(None,), dtype='f')
q_ = f.create_dataset('q', (1,)+q.shape, maxshape=(None,)+q.shape, dtype='f', compression="lzf")

t_[0] = 0.0
i_[0] = 0
q_[0] = q
