import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", type=str, help="input file utility matrix")
parser.add_argument("metrics", type=str, help="input selected metric")
parser.add_argument("neighbors", type=int, help="input number of neighbors")
parser.add_argument("prediction", type=str, help="input type of prediction")
args = parser.parse_args()
print(args.file)
print(args.metrics)

# Leer un fichero
A = np.loadtxt(args.file, dtype=str)

print(int(A[0][0])+1)
