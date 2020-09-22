import numpy as np
from fes.FES1DL21 import FES1DL21
from mesh.MeshGenerator import line1DL2
from numerics.SparseMatrix import SMatrix
from scipy.sparse.linalg import *
mesh = line1DL2(0.0, 1.0, 10)
mesh.printNodes()
mesh.printElements()
mesh.printBoundaries()
print(mesh.nodes)
print(mesh.elements)
print(mesh.boundaries)
