import numpy as np
from fes.FES1DL21 import FES1DL21
from mesh.MeshGenerator import line1DL2
from numerics.SparseMatrix import SMatrix
from scipy.sparse.linalg import *
from scipy import linalg
import matplotlib.pyplot as plt


# 求三角形的面积
def area3(x, y):
    S = 0
    for i in range(2):
        S = S + x[i] * y[i + 1] - x[i + 1] * y[i]
    S = S + x[2] * y[0] - x[0] * y[2]
    S = S / 2
    return S

# x = np.array([0, 1, 0])
# y = np.array([0, 0, 1])
# S = area3(x, y)


# 第三章
p = np.array([[0, 1, 2, 2, 0], [0, 0, 0, 1, 1]])
n_p = 5
t = np.array([[1, 1, 2], [4, 2, 3], [5, 4, 4]])
n_t = 3
M = np.zeros((n_p, n_p))
b = np.zeros(n_p)


def fun(x, y):
    f = x * y
    return f


x = np.array([0, 0, 0])
y = np.array([0, 0, 0])
for i in range(n_t):
    ele = t[:, i]
    for ii in range(3):
        x[ii] = p[0, ele[ii] - 1]
        y[ii] = p[1, ele[ii] - 1]

    S = area3(x, y)
    MK = np.array([[2, 1, 1], [1, 2, 1], [1, 1, 2]])
    for j in range(3):
        for v in range(3):
            M[ele[j] - 1, ele[v] - 1] += MK[j, v] * S / 12

    hK = np.array([[fun(x[0], y[0]) / 3], [fun(x[1], y[1]) / 3], [fun(x[2], y[2]) / 3]])
    for u in range(3):
        b[ele[u] - 1] += hK[u] * S

Pf = linalg.solve(M, b)
print(Pf)


# 生成网格的结点坐标，三角单元和区域边界
# m,n分别为x,y的划分，[a,b]和[c,d]分别为x,y的取值范围
def NODES1(m, n, a, b, c, d):
    nodes1 = np.zeros(((m + 1) * (n + 1), 2))  # 结点坐标
    for i in range(n + 1):
        for j in range(m + 1):
            nodes1[i * (m + 1) + j, 0] = j
            nodes1[i * (m + 1) + j, 1] = i

    for iii in range((m + 1) * (n + 1)):
        nodes1[iii, 0] = nodes1[iii, 0] * (b - a) / m + a
        nodes1[iii, 1] = nodes1[iii, 1] * (d - c) / n + c
    print(nodes1)


def ELEMENTS1(m, n, a, b, c, d):
    elements1 = np.zeros((2 * m * n, 3))  # 三角单元
    for ii in range(n):
        for jj in range(m):
            elements1[(ii * m + jj) * 2 + 0, :] = [ii * (m + 1) + jj,
                                                   ii * (m + 1) + jj + 1,
                                                   (ii + 1) * (m + 1) + jj + 1]
            elements1[(ii * m + jj) * 2 + 1, :] = [ii * (m + 1) + jj,
                                                   (ii + 1) * (m + 1) + jj + 1,
                                                   (ii + 1) * (m + 1) + jj]
    print(elements1)


def BOUNDARIES1(m, n, a, b, c, d):
    boundaries1 = np.zeros((2 * (m + n), 3))  # 区域边界
    for k in range(m):
        boundaries1[k, :] = [k, k + 1, 1]
        boundaries1[k + m + n, :] = [(m + 1) * n + k, (m + 1) * n + k + 1, 3]
    for kk in range(n):
        boundaries1[kk + m, :] = [(m + 1) * kk + m, (m + 1) * (kk + 1) + m, 2]
        boundaries1[kk + 2 * m + n, :] = [(m + 1) * kk, (m + 1) * (kk + 1), 4]
    print(boundaries1)


NODES1(5, 6, 2, 4, 2, 5)  # 结点坐标
ELEMENTS1(5, 6, 2, 4, 2, 5)  # 三角单元
BOUNDARIES1(5, 6, 2, 4, 2, 5)  # 区域边界

