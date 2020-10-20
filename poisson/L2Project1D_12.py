import numpy as np
from fes.FES1DL21 import FES1DL21
from mesh.MeshGenerator import line1DL2
from numerics.SparseMatrix import SMatrix
from scipy.sparse.linalg import *
from scipy import linalg
import matplotlib.pyplot as plt

# 第二章
n = 60
A = np.zeros((n + 1, n + 1))
b = np.zeros((n + 1))
g = np.array([-1, 0])
kappa = np.array([1e+06, 0])
mesh = line1DL2(2.0, 8.0, n)
mesh.printNodes()
mesh.printElements()
mesh.printBoundaries()

a = lambda x: 0.1 * (5 - 0.6 * x)
f = lambda x: 0.03 * (x - 6) ** 4

for i in range(n):
    ele = mesh.elements[i, :]
    x = mesh.nodes[ele, :]
    h = x[1] - x[0]
    x_mid = (x[1]+x[0])/2
    hm = np.array([[1, -1], [-1, 1]])
    for j in range(2):
        for v in range(2):
            A[ele[j], ele[v]] += hm[j, v] * a(x_mid) / h
    A[0, 0] += kappa[0]
    A[n, n] += kappa[1]

    hb = np.array([[f(x[0]) * h / 2], [f(x[1]) * h / 2]])
    for u in range(2):
        b[ele[u]] += hb[u]
    b[0] += kappa[0] * g[0]
    b[n] += kappa[1] * g[1]

u = linalg.solve(A, b)
print(u)

# plt.figure()
plt.plot(mesh.nodes, u, 'r-')
# plt.plot(x, y)
plt.show()

