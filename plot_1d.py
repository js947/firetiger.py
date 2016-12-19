import pickle
import argparse
import numpy as np
import h5py
import matplotlib.pyplot as plt

from eos import IdealGas
from euler import Euler

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("file", help="file to read", type=str)
parser.add_argument("variable", help="variable to plot", default="pressure", type=str)
parser.add_argument("-i", help="step number to plot", default=-1, type=int)
parser.add_argument("-o", help="output file")
args = parser.parse_args()

f = h5py.File(args.file, 'r')
sys = np.loads(f.attrs['system'])
D = len(f['h'])

x = [f[n] for (n,i) in zip("xyz",range(0,D))]
q = getattr(sys, args.variable)(f['q'][args.i])

if D == 1:
    plt.plot(x[0], q, '.-')
    plt.title("%s @ %d:%f" % (args.file, f['i'][args.i], f['t'][args.i]))
    plt.ylabel("%s" % args.variable)
elif D == 2:
    plt.axis('equal')
    plt.contourf(x[0], x[1], q, 15)
    plt.colorbar()
    plt.title("%s %s @ %d:%f" % (args.file, args.variable, f['i'][args.i], f['t'][args.i]))

if args.o:
    plt.savefig(args.o)
else:
    plt.show()
