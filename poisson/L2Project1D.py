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
n=5
M=np.zeros((n+1, n+1))
b=np.zeros((n+1, 1))
def f(x):
    return 2*x*np.sin(2*np.pi*x)+3
g = lambda x: 2*x*np.sin(2*np.pi*x)+3

for i in range(n):
    ele = mesh.elements[i, :]
    xy = mesh.nodes[ele, :]
#    print(xy)
    h=xy[1, 0] - xy[0, 0]
    eleMatrix = np.array([[h/3, h/6], [h/6, h/3]])
    for ii in range(2):
        for jj in range(2):
            M[ele[ii], ele[jj]] += eleMatrix[ii, jj]
    # M[i,i]=M[i,i]+h/3
    # M[i,i+1] = M[i,i+1] + h / 6
    # M[i+1,i] = M[i+1,i] + h / 6
    # M[i+1,i+1] = M[i+1,i+1] + h / 3
for i in range(n):
    #h = mesh.nodes[i + 1] - mesh.nodes[i]
    ele = mesh.elements[i, :]
    xy = mesh.nodes[ele, :]
    #    print(xy)
    h = xy[1, 0] - xy[0, 0]
    eleVec = np.array([f(xy[0, 0])*h/2, f(xy[1, 0])*h/2])
#    print(eleVec)
#    b[ele] += eleVec
    b[ele[0]] += eleVec[0] # +f(mesh.nodes[i])*h/2
    b[ele[1]] += eleVec[1] # +f(mesh.nodes[i+1])*h/2
# print(b)
Pf=np.linalg.inv(M).dot(b)
print(np.linalg.inv(M))
print(Pf)
mesh.plotSolution(Pf, 'x', 'y', 'kesai')

