import numpy as np
from scipy.linalg import eig, eigh
from scipy.sparse.linalg import eigs, eigsh
from numerics.SparseMatrix import SMatrix
# np.set_printoptions(suppress=True)
# np.random.seed(0)
# X = np.random.random((10,10)) - 0.5
# X = np.dot(X, X.T) #create a symmetric
# #print(X)
# evals_all, evecs_all = eigh(X)
# print(evals_all)
n = 1000
A = SMatrix(row=n+1, col=n+1)
M = SMatrix(row=n+1, col=n+1)
for i in range(n):
    for j in range(n):
        if i == j:
            A.setElement(i, j, 2 * n)
            M.setElement(i, j, 2.0 / (3 * n))
        elif np.abs(i - j) == 1:
            A.setElement(i, j, -n)
            M.setElement(i, j, 1.0 / (6 * n))
A.setElement(0, 0, 1.0e30)
A.setElement(n, n, 1.0e30)
A.sort()
A.printMatrix()
M.setElement(0, 0, 1.0 / (3 * n))
M.setElement(n, n, 1.0 / (3 * n))
M.sort()
M.printMatrix()

AS = A.toCSC_Matrix()
MS = M.toCSC_Matrix()
evalues, evectors = eigsh(AS, 10, MS, sigma=0)
print(evalues)


