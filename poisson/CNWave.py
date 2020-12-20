import numpy as np
import torch
from scipy.sparse.linalg import factorized

from fes.ComputationalGeometry import area2DT3, gradient2DT3
from fes.FES2DT31 import FES2DT31
from mesh.MeshGenerator import readMesh2T3
from numerics.SparseMatrix import SMatrix

mesh = readMesh2T3("..\meshfile\meshwave.txt")
mesh.plotMesh()
nodes = mesh.nodes
elements = mesh.elements

fs = FES2DT31(mesh)
nDof = fs.nDof  # 2968
A = np.zeros((nDof, nDof))
M = np.zeros((nDof, nDof))

xy = np.zeros((3,2))
for i in range(len(elements)):
    ele = elements[i, :]
    for ii in range(3):
        xy[ii, 0] = nodes[ele[ii] - 1, 0]
        xy[ii, 1] = nodes[ele[ii] - 1, 1]

    S = area2DT3(xy)
    grad = gradient2DT3(xy)
    b = grad[0][:, 0]
    c = grad[0][:, 1]
    AK = np.array([[b[0]*b[0]+c[0]*c[0], b[0]*b[1]+c[0]*c[1], b[0]*b[2]+c[0]*c[2]],
                   [b[1]*b[0]+c[1]*c[0], b[1]*b[1]+c[1]*c[1], b[1]*b[2]+c[1]*c[2]],
                   [b[2]*b[0]+c[2]*c[0], b[2]*b[1]+c[2]*c[1], b[2]*b[2]+c[2]*c[2]]])
    MK = np.array([[2, 1, 1], [1, 2, 1], [1, 1, 2]])
    for j in range(3):
        for v in range(3):
            A[ele[j] - 1, ele[v] - 1] += AK[j, v] * S
            M[ele[j] - 1, ele[v] - 1] += MK[j, v] * S / 12

RHS = np.zeros(nDof)

K = 0.005
xi = np.zeros(nDof)
eta = np.zeros(nDof)
for k in range(400):
    time = 1 * 0.005
    LHS = np.vstack((np.hstack((M, -0.5 * k * M)), np.hstack((0.5 * k * A, M))))
    LHS_0 = np.vstack((np.hstack((M, 0.5 * k * M)), np.hstack((-0.5 * k * A, M))))
    rhs = np.dot(LHS_0, np.hstack((xi, eta))) + np.hstack((np.zeros(nDof), k * RHS))
    # LHS = [[M, -0.5 * k * M], [0.5 * k * A, M]]
    # rhs = [[M, 0.5 * k * M], [-0.5 * k * A, M]] * [[xi], [eta]] + [[np.zeros(nDof)],[k * RHS]]
    # solve = factorized(LHS.toCSC_Matrix())
    # x = solve(rhs)
    Pf = np.linalg.solve(LHS, rhs)
    # print(Pf)
    Pf_0 = np.hsplit(Pf, 2)
    xi = Pf_0[0]
    eta = Pf_0[1]
    xii = np.where(xi < -0.249999)
    xi[xii] = 0.1 * np.sin(8 * np.pi * time)

    # print(np.min(Pf), np.max(Pf))

mesh.plotSolution(xi)
