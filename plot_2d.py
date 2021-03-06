#!/usr/bin/env python3
import pickle
import argparse
import numpy as np
import h5py
import matplotlib.pyplot as plt

from eos import IdealGas
from euler import Euler

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("file", help="file to read", type=str)
parser.add_argument("variable", help="variable to plot", type=str)
parser.add_argument("-i", help="step number to plot", default=-1, type=int)
parser.add_argument("-o", help="output file")
parser.add_argument('-min', help='min range', default=None, type=float)
parser.add_argument('-max', help='max range', default=None, type=float)
args = parser.parse_args()

f = h5py.File(args.file, 'r', libver='latest', swmr=True)
sys = np.loads(f.attrs['system'])
D = len(f['h'])

x = f['x']
q = sys.expr(args.variable)(f['q'][args.i])

plt.axis('equal')
plt.contourf(x[0], x[1], q, 15)
#plt.pcolor(x[0], x[1], q, vmin=args.min, vmax=args.max)
plt.colorbar()
plt.title("%s %s @ %d:%f" % (args.file, args.variable, f['i'][args.i], f['t'][args.i]))
plt.tight_layout()

if args.o:
    plt.savefig(args.o)
else:
    plt.show()
