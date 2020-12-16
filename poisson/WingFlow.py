import numpy as np
from scipy.sparse.linalg import factorized

from fes.FES2DT31 import FES2DT31
from mesh.MeshGenerator import readMesh2T3
from numerics.SparseMatrix import SMatrix

mesh = readMesh2T3("..\meshfile\meshWing.txt")
mesh.plotMesh()
fs = FES2DT31(mesh)
nDof = fs.nDof
A = SMatrix(size=nDof)

fs.assembleStiff(np.array([1.0]), None, "COMMON", A)
RHS = np.zeros(nDof)

fs.assembleFlux(np.array([1.0]), None, "COMMON", RHS, [17])
fs.applyBC_MBN_MR(A, RHS, "x", 0.0, None, [15])
solve = factorized(A.toCSC_Matrix())
x = solve(RHS)
print(np.min(x), np.max(x))
mesh.plotSolution(x)


