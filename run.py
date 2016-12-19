from __future__ import print_function
import pickle
import argparse
import numpy as np
import h5py

from eos import IdealGas
from euler import Euler
from solver import cfl, update

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("file", help="simulation file", type=str)
parser.add_argument("-t", help="simulation length", default=1, type=float)
parser.add_argument("-n", help="number of steps", default=None, type=int)
args = parser.parse_args()

f = h5py.File(args.file, 'r+')
sys = np.loads(f.attrs['system'])

i_all, t_all, q_all = (f[n] for n in "itq")
h = f['h']

i, t, q = (x[-1] for x in (i_all, t_all, q_all))

D = len(q.shape)-1

while (t < args.t) and (not args.n or i < args.n):
    dt = cfl(D, sys, h, q, cfl=0.95)
    print("%5i %12f %12f" % (i, t, dt))
    q = update(D, sys, h, dt, q)
    i += 1
    t += dt
print("%5i %12f" % (i, t))

for dat in (i_all, t_all, q_all):
    dat.resize(dat.shape[0]+1, axis=0)

i_all[-1], t_all[-1], q_all[-1] = i, t, q
