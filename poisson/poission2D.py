import numpy as np
from fes.FES2DT31 import FES2DT31
from mesh.MeshGenerator import square2D
from numerics.SparseMatrix import SMatrix
from scipy.sparse.linalg import *
mesh = square2D(100, 100, 1)
fs = FES2DT31(mesh)
nDof = fs.nDof
A = SMatrix(size=nDof)

fs.assembleStiff(np.array([1.0]), None, "COMMON", A)
# A.sort()
# A.printMatrix()
RHS = np.zeros(nDof)
#f = lambda xy, label, param: np.sin(2 * np.pi * xy[0]) * np.cos(2 * np.pi * xy[1])
#fs.assembleSource_func([f], None, "COMMON", RHS)
# print(RHS)
# nodes = mesh.getBoundariesNodes([1, 2, 3, 4])
# print(nodes)

# A.setElement(0, 0, 1.0e30)
# A.setElement(nDof-1, nDof-1, 1.0e30)
# RHS[0] = 0
# RHS[-1] = 0
# print(RHS)
bdFunc = lambda xy, label, param : np.sin(2 * np.pi * xy[0])
fs.applyBC_MBN_MR(A, RHS, "x", bdFunc, None, [1, 2, 3, 4])
#A.printMatrix()
solve = factorized(A.toCSC_Matrix())
x = solve(RHS)
print(np.min(x), np.max(x))
# print(x)
mesh.plotSolution(x)