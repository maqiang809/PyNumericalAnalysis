import numpy as np
from fes.ComputationalGeometry import area2DT3, gradient2DT3
from fes.FES2DT31 import FES2DT31
from mesh.MeshGenerator import readMesh2T3
from numerics.SparseMatrix import SMatrix

mesh = readMesh2T3("..\meshfile\meshwave.txt")
mesh.plotMesh()
nodes = mesh.nodes
xii = np.where(nodes[:, 0] < -0.249999)  # Dirichlet nodes
elements = mesh.elements

fs = FES2DT31(mesh)
nDof = fs.nDof  # 2968
A = np.zeros((nDof, nDof))
M = np.zeros((nDof, nDof))
B = np.zeros(nDof)

def f(x, y):
    f = 0
    return f


xy = np.zeros((3, 2))
for i in range(len(elements)):
    ele = elements[i, :]
    for ii in range(3):
        xy[ii, 0] = nodes[ele[ii], 0]
        xy[ii, 1] = nodes[ele[ii], 1]

    S = area2DT3(xy)
    grad = gradient2DT3(xy)
    # print(grad)
    b = grad[0][:, 0]
    c = grad[0][:, 1]
    AK = np.array([[b[0]*b[0]+c[0]*c[0], b[0]*b[1]+c[0]*c[1], b[0]*b[2]+c[0]*c[2]],
                   [b[1]*b[0]+c[1]*c[0], b[1]*b[1]+c[1]*c[1], b[1]*b[2]+c[1]*c[2]],
                   [b[2]*b[0]+c[2]*c[0], b[2]*b[1]+c[2]*c[1], b[2]*b[2]+c[2]*c[2]]])
    MK = np.array([[2, 1, 1], [1, 2, 1], [1, 1, 2]])
    for j in range(3):
        for v in range(3):
            A[ele[j], ele[v]] += AK[j, v] * S
            M[ele[j], ele[v]] += MK[j, v] * S / 12
    hK = np.array([[f(xy[0, 0], xy[0, 1]) / 3], [f(xy[1, 0], xy[1, 1]) / 3], [f(xy[2, 0], xy[2, 1]) / 3]])
    for u in range(3):
        B[ele[u]] += hK[u] * S

k = 0.005  # time step
T = 2  # final time
xi = np.zeros(nDof)
eta = np.zeros(nDof)
for h in range(int(T/k)):
    time = k * h
    LHS = np.vstack((np.hstack((M, -0.5 * k * M)), np.hstack((0.5 * k * A, M))))
    LHS_0 = np.vstack((np.hstack((M, 0.5 * k * M)), np.hstack((-0.5 * k * A, M))))
    rhs = np.dot(LHS_0, np.hstack((xi, eta))) + np.hstack((np.zeros(nDof), k * B))
    # LHS = [[M, -0.5 * k * M], [0.5 * k * A, M]]
    # rhs = [[M, 0.5 * k * M], [-0.5 * k * A, M]] * [[xi], [eta]] + [[np.zeros(nDof)],[k * RHS]]

    Pf = np.linalg.solve(LHS, rhs)
    # print(Pf)
    Pf_0 = np.hsplit(Pf, 2)
    xi = Pf_0[0]
    eta = Pf_0[1]
    xi[xii] = 0.1 * np.sin(8 * np.pi * time)

    # print(np.min(Pf), np.max(Pf))

mesh.plotSolution(xi)
