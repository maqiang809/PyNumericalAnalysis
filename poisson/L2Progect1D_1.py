import numpy as np
from fes.FES1DL21 import FES1DL21
from mesh.MeshGenerator import line1DL2
from numerics.SparseMatrix import SMatrix
from scipy.sparse.linalg import *
from scipy import linalg
import matplotlib.pyplot as plt

# 第一章
mesh = line1DL2(0.0, 1.0, 10)
mesh.printNodes()
mesh.printElements()
mesh.printBoundaries()
n = 10
m = np.zeros((n + 1, n + 1))
b = np.zeros((n + 1))

g = lambda x: x * np.sin(x)
# def f(x):
#     return x * np.sin(x)

for i in range(n):
    ele = mesh.elements[i, :]
    x = mesh.nodes[ele, :]
    h = x[1] - x[0]
    hm = np.array([[h / 3, h / 6], [h / 6, h / 3]])
    for j in range(2):
        for v in range(2):
            m[ele[j], ele[v]] += hm[j, v]

    hb = np.array([[g(x[0]) * h / 2], [g(x[1]) * h / 2]])
    for u in range(2):
        b[ele[u]] += hb[u]
# print(m)
# print(b)

Pf = linalg.solve(m, b)
print(Pf)

plt.plot(mesh.nodes, Pf, 'r-o')
# plt.plot(x, y)
plt.show()
