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
parser.add_argument("-o", help="output file")
args = parser.parse_args()

f = h5py.File(args.file, 'r')
sys = np.loads(f.attrs['system'])
D = len(f['h'])

x = f['x']
q = np.stack(sys.expr(args.variable)(q) for q in f['q'])

plt.contourf(x[0], f['t'], q, 15)

plt.title("%s %s" % (args.file, args.variable))
plt.xlabel('x')
plt.ylabel('t')

if args.o:
    plt.savefig(args.o)
else:
    plt.show()
