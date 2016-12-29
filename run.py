#!/usr/bin/env python3
import pickle
import argparse
import numpy as np
import h5py
from time import time

from eos import IdealGas, StiffenedGas
from euler import Euler
from multiphase import Multiphase

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("file", type=str,   help="simulation file")
parser.add_argument("-i",   type=int,   help="simulation start", default=-1)
parser.add_argument("-t",   type=float, help="simulation end time", default=1)
parser.add_argument("-n",   type=int,   help="number of steps to run", default=None)
parser.add_argument("-oi",  type=int,   help="number of steps between outputs", default=None)
parser.add_argument("-cfl", type=float, help="cfl number", default=0.95)
parser.add_argument("-p",   type=np.dtype, help="type to do calculations", default=np.dtype('f8'))

output_ctrl = parser.add_mutually_exclusive_group(required=False)
output_ctrl.add_argument("-of", help="time between outputs", default=None, type=float)
output_ctrl.add_argument("-on", help="number of (equally spaced) output steps", default=None, type=int)

args = parser.parse_args()

f = h5py.File(args.file, 'r+')
sys = np.loads(f.attrs['system'])

h, q_all, i_all, t_all = (f[n] for n in "hqit")
q, i, t = (x[args.i].astype(args.p) for x in (q_all, i_all, t_all))
if not args.p.isnative:
    print("warning: using non native data type")

np.seterr(**{t:'raise' for t in ('divide', 'over', 'invalid')})

def advance(q, i, t, dt):
    print("%5i %12f %12f" % (i, t, dt), end='')
    a = time()
    ans = sys.update(q, h, dt), i+1, t+dt
    b = time()
    print(" %12f" % (b-a))
    return ans

def output(q, i, t):
    print("%5i %12f output" % (i, t))
    for dat in (i_all, t_all, q_all):
        dat.resize(dat.shape[0]+1, axis=0)
    i_all[-1], t_all[-1], q_all[-1] = i, t, q

if args.on:
    target_times = np.linspace(t, args.t, args.on)[1:]
else:
    target_times = np.append(np.arange(t, args.t, args.of)[1:], args.t)

for tn in target_times:
    while not args.n or i < args.n:
        try:
            dt = sys.cfl(q, h, cfl=args.cfl)

            if t + dt > tn:
                output(*advance(q, i, t, tn - t))
                break

            q, i, t = advance(q, i, t, dt)

            if args.oi and i%args.oi:
                output(q, i, t)
        except FloatingPointError:
            print('caught floating point exception', file=stderr)
            output(q, i, t)
            exit(1)
