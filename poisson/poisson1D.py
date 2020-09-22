import numpy as np
from fes.FES1DL21 import FES1DL21
from mesh.MeshGenerator import line1DL2
from numerics.SparseMatrix import SMatrix
from scipy.sparse.linalg import *
mesh = line1DL2(0.0, 1.0, 100)
fs = FES1DL21(mesh)
nDof = fs.nDof
A = SMatrix(size=nDof)
fs.assembleStiff_const([1.0], "COMMON", A)
A.sort()
A.printMatrix()
RHS = np.zeros(nDof)
fs.assembleSource_const([1.0], "COMMON", RHS)
print(RHS)
nodes = mesh.getBoundariesNodes([1, 2])
print(nodes)

# A.setElement(0, 0, 1.0e30)
# A.setElement(nDof-1, nDof-1, 1.0e30)
# RHS[0] = 0
# RHS[-1] = 0
print(RHS)

fs.applyBC_MBN_Const(A, RHS, "x", 0.0, None, [1])
fs.applyBC_MBN_Const(A, RHS, "x", 1.0, None, [2])
A.printMatrix()
solve = factorized(A.toCSC_Matrix())
x = solve(RHS)
print(x)
mesh.plotSolution(x, 'x', 'y', 'Temperature')




