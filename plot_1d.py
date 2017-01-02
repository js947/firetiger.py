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
parser.add_argument("variable", help="variable to plot", type=str, nargs='+')
parser.add_argument("-i", help="step number to plot", default=-1, type=int)
parser.add_argument("-o", help="output file")
args = parser.parse_args()

f = h5py.File(args.file, 'r')
sys = np.loads(f.attrs['system'])
D = len(f['h'])

x = f['x']

plt.title("%s @ %d:%f" % (args.file, *[f[n][args.i] for n in "it"]))
for q,v in [(sys.expr(v)(f['q'][args.i]),v) for v in args.variable]:
    plt.plot(x[0], q, '.-', label=v)
if len(args.variable) == 1:
    plt.ylabel("%s" % args.variable[0])
else:
    plt.legend()
plt.tight_layout()

if args.o:
    plt.savefig(args.o)
else:
    plt.show()
