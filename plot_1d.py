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
args = parser.parse_args()

f = h5py.File(args.file, 'r')
sys = np.loads(f.attrs['system'])
D = len(f['h'])

x = [f[n] for (n,i) in zip("xyz",range(0,D))]
q = getattr(sys, args.variable)(f['q'][args.i])

plt.plot(x[0], q, '.-')
plt.title("%s @ %d:%f" % (args.file, f['i'][args.i], f['t'][args.i]))
plt.ylabel("%s" % args.variable)

if args.o:
    plt.savefig(args.o)
else:
    plt.show()