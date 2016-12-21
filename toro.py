import pickle
import argparse
import numpy as np
import h5py

from eos import IdealGas
from euler import Euler

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-x", help="x resolution", default=200, type=int)
parser.add_argument("-c", help="test case", default=1, type=int)
parser.add_argument("-o", help="simulation file", default="toro.h5", type=str)
args = parser.parse_args()

sys = Euler(IdealGas(1.4))

def coord(x0, x1, nx):
    x, dx = np.linspace(x0, x1, nx+1, retstep=True)
    x += dx/2
    return x[:-1], dx

x, dx = coord(0.0, 1.0, args.x)

qL = { 1: sys.cons(1.0, 1.0, 0.75)
     , 2: sys.cons(1.0, 0.4, -2.0)
     , 3: sys.cons(1.0, 1000.0, 0.0)
     , 4: sys.cons(5.99924, 460.894, 19.5975)
     , 5: sys.cons(1.0,1000.0,-19.59745)
     }
qR = { 1: sys.cons(0.125, 0.1, 0.0)
     , 2: sys.cons(1.0,0.4,2.0)
     , 3: sys.cons(1.0,0.01,0.0)
     , 4: sys.cons(5.99242, 46.095, -6.19633)
     , 5: sys.cons(1.0,0.01,-19.59745)
     }
m =  { 1: 0.3
     , 2: 0.5
     , 3: 0.5
     , 4: 0.3
     , 5: 0.8
     }

q = np.where(x < m[args.c], qL[args.c][:,None], qR[args.c][:,None])

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
