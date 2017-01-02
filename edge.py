#!/usr/bin/env python3
import pickle
import argparse
import numpy as np
import h5py
import matplotlib.pyplot as plt
from matplotlib import cm
from sklearn.preprocessing import normalize
from skimage.exposure import equalize_adapthist
from skimage.filters import scharr, threshold_isodata as threshold
from skimage.transform import probabilistic_hough_line

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

edges = scharr(normalize(q))
edges = np.where(edges >= threshold(edges), 1, 0)
#lines = probabilistic_hough_line(edges)

plt.pcolormesh(x[0], f['t'], edges)
plt.colorbar()

plt.title("%s %s edges" % (args.file, args.variable))
plt.xlabel('x')
plt.ylabel('t')

#for (p0, p1) in lines:
    #plt.plot((p0[0], p1[0]), (p0[1], p1[1]))

if args.o:
    plt.savefig(args.o)
else:
    plt.show()
