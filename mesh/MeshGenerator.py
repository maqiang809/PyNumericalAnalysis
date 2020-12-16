from mesh.Mesh1DL import Mesh1DL2
from mesh.Mesh2DT import Mesh2DT3
import numpy as np

def line1DL2(a, b, num):
    mesh = Mesh1DL2()
    nv = num + 1
    nt = num
    nb = 2
    mesh.initMesh0(nv, nt, nb)
    for i in range(nv):
        mesh.nodes[i, 0] = a + (b - a) / num * i
    for i in range(nt):
        mesh.elements[i, 0] = i
        mesh.elements[i, 1] = i + 1
    mesh.boundaries[0, 0] = 0
    mesh.boundaryLabel[0] = 1
    mesh.boundaries[1, 0] = num
    mesh.boundaryLabel[1] = 2
    return mesh

def square2D(xNum, yNum, T3Type):
    mesh = Mesh2DT3()
    nv = (xNum + 1) * (yNum + 1)
    nt = 2 * xNum * yNum
    nb = 2 * (xNum + yNum)
    mesh.initMesh0(nv, nt, nb)
    idx = 0
    for i in range(yNum + 1):
        for j in range(xNum + 1):
            mesh.nodes[idx] = [(j + 0.0) / xNum, (i + 0.0) / yNum]
            idx += 1
    createSquareElements(mesh, xNum, yNum, T3Type)
    createSquareBoundarys(mesh, xNum, yNum)
    return mesh


def createSquareElements(mesh, xNum, yNum, T3Type):
    ti1 = 0
    tj1 = 0
    tk1 = 0
    ti2 = 0
    tj2 = 0
    tk2 = 0
    idx = 0
    for i in range(yNum):
        for j in range(xNum):
            ti1 = i * (xNum + 1) + j
            if T3Type == 1:
                tj1 = ti1 + 1
                tk1 = tj1 + xNum + 1
                ti2 = i * (xNum + 1) + j
                tj2 = ti2 + xNum + 1 + 1
                tk2 = tj2 - 1
            elif T3Type == 2:
                tj1 = ti1 + 1
                tk1 = ti1 + xNum + 1
                ti2 = i * (xNum + 1) + j + 1
                tj2 = ti2 + xNum + 1
                tk2 = tj2 - 1
            elif T3Type == 3:
                if (i + j) % 2 == 0:
                    tj1 = ti1 + 1
                    tk1 = ti1 + xNum + 1
                    ti2 = i * (xNum + 1) + j + 1
                    tj2 = ti2 + xNum + 1
                    tk2 = tj2 - 1
                else:
                    tj1 = ti1 + 1
                    tk1 = tj1 + xNum + 1
                    ti2 = i * (xNum + 1) + j
                    tj2 = ti2 + xNum + 1 + 1
                    tk2 = tj2 - 1
            elif T3Type == 4:
                if (i + j) % 2 == 1:
                    tj1 = ti1 + 1
                    tk1 = ti1 + xNum + 1
                    ti2 = i * (xNum + 1) + j + 1
                    tj2 = ti2 + xNum + 1
                    tk2 = tj2 - 1
                else:
                    tj1 = ti1 + 1
                    tk1 = tj1 + xNum + 1
                    ti2 = i * (xNum + 1) + j
                    tj2 = ti2 + xNum + 1 + 1
                    tk2 = tj2 - 1
            else:
                raise TypeError("Unexpected Triangle Type, not in 1, 2, 3, 4!")
            mesh.elements[idx] = [ti1, tj1, tk1]
            idx += 1
            mesh.elements[idx] = [ti2, tj2, tk2]
            idx += 1

def createSquareBoundarys(mesh, xNum, yNum):
    idx = 0
    for i in range(xNum):
        mesh.boundaries[idx], mesh.boundaryLabel[idx] = [i, i + 1], 1
        idx += 1
    for i in range(yNum):
        local = xNum + i * (xNum + 1);
        mesh.boundaries[idx], mesh.boundaryLabel[idx] = [local, local + xNum + 1], 2
        idx += 1
    for i in range(xNum):
        local = xNum + yNum * (xNum + 1) - i
        mesh.boundaries[idx], mesh.boundaryLabel[idx] = [local, local - 1], 3
        idx += 1
    for i in range(yNum):
        local = (yNum - i) * (xNum + 1)
        mesh.boundaries[idx], mesh.boundaryLabel[idx] = [local, local - (xNum + 1)], 4
        idx += 1

def readMesh2T3(fileName):
    f = open(fileName, 'r')
    line = f.readline()
    list = line.split()
    nv = int(list[0])
    nt = int(list[1])
    nb = int(list[2])
    mesh = Mesh2DT3()
    mesh.initMesh0(nv, nt, nb)
    for i in range(nv):
        node = f.readline().split()
        mesh.nodes[i, 0] = float(node[0])
        mesh.nodes[i, 1] = float(node[1])
        mesh.nodeLabel[i] = int(node[2])
    for i in range(nt):
        element = f.readline().split()
        mesh.elements[i, 0] = int(element[0]) - 1
        mesh.elements[i, 1] = int(element[1]) - 1
        mesh.elements[i, 2] = int(element[2]) - 1
        mesh.elementLabel[i] = int(element[3])
    for i in range(nb):
        boundary = f.readline().split()
        mesh.boundaries[i, 0] = int(boundary[0]) - 1
        mesh.boundaries[i, 1] = int(boundary[1]) - 1
        mesh.boundaryLabel[i] = int(boundary[2])
    return mesh

# mesh = square2D(4, 4, 1)
# mesh.printBoundaries()
# nodes = mesh.getBoundariesNodes([2])
# print(nodes)

# mesh = square2D(20, 20, 1)
# myFunc = lambda xy : np.sin(2 * np.pi * xy[0]) * np.sin(2 * np.pi * xy[1])
# u = mesh.meshfunc(myFunc)
# mesh.printNodes()
# mesh.printElements()
# mesh.printBoundaries()
# mesh.plotMesh()
# mesh.plotSolution(u)
#
# A = np.array([[1, 2], [3, 4]])
# B = np.array([[5, 6], [7, 8]])
# C = np.dot(A, B)
# print(C)
# mesh = line1DL2(0.0, 1.0, 10)
# # mesh.printNodes()
# # mesh.printElements()
# # mesh.printBoundaries()
#
# print(mesh.NumberOfNodes)
# print(mesh.NumberOfElements)
# print(mesh.NumberOfBoundaries)
# mesh.saveMesh("mymesh1D.txt")
# print(mesh.NumberOfNodes)
