#!/usr/bin/env python3
import pickle
import argparse
import numpy as np
import h5py
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("file", help="file to read", type=str)
parser.add_argument('-i', help='index to slice at', type=int)
parser.add_argument("-o", help="output file")
args = parser.parse_args()

f = h5py.File(args.file, 'r')
g = h5py.File(args.o, 'w')
g.attrs['system'] = f.attrs['system']

g.create_dataset('h', data=f['h'][0:1])
g.create_dataset('t', data=f['t'])
g.create_dataset('i', data=f['i'])
g.create_dataset('q', data=f['q'][:,:,args.i])
g.create_dataset('x', data=f['x'][0:1,args.i])
