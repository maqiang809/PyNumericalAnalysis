import numpy as np
import abc
import matplotlib.pyplot as plt

class Mesh2D3T:
    def __init__(self):
        self.nv = 0
        self.nt = 0
        self.nb = 0
        self.nDim = 2
        self.nPerElement = 3
        self.nPerBoundary = 2
        self.tecplotType = ""#?
        self.nodes = None
        self.nodeLabel = None
        self.elements = None
        self.elementLabel = None
        self.boundaries = None
        self.boundaryLabel = None

    def scale(self, sx, sy):
        for i in range(self.nv):
            x = self.nodes[i, 0]
            y = self.nodes[i, 1]
            self.nodes[i, 0] = sx * x
            self.nodes[i, 0] = sy * y
    def initMesh0(self, nv, nt, nb):
        self.nv = nv
        self.nt = nt
        self.nb = nb
        self.nodes = np.zeros((self.nv, self.nDim), dtype=np.float)
        self.nodeLabel = np.zeros(self.nv, dtype=np.int32)
        self.elements = np.zeros((self.nt, self.nPerElement), dtype=np.int32)
        self.elementLabel = np.zeros(self.nt, dtype=np.int32)
        self.boundaries = np.zeros((self.nb, self.nPerBoundary), dtype=np.int32)
        self.boundaryLabel = np.zeros(self.nb, dtype=np.int32)

    def printNodes(self):
        for i in range(self.nv):
            for j in range(self.nDim):
                print('%.16f' % self.nodes[i, j], end='\t')
            print(self.nodeLabel[i])

    def printElements(self):
        for i in range(self.nt):
            for j in range(self.nPerElement):
                print('%10d' % self.elements[i, j], end='\t')
            print(self.elementLabel[i])

    def printBoundaries(self):
        for i in range(self.nb):
            for j in range(self.nPerBoundary):
                print('%10d' % self.boundaries[i, j], end='\t')
            print(self.boundaryLabel[i])

    def plotMesh(self):
        plt.figure()
        plt.gca().set_aspect('equal')
        plt.triplot(self.nodes[:, 0], self.nodes[:, 1], self.elements, lw=0.6, color='k')
        plt.show()


def rectangle2D(xNum, yNum, xLength,yWide):
    mesh = Mesh2D3T()
    nv = (xNum + 1) * (yNum + 1)
    nt = 2 * xNum * yNum
    nb = 2 * (xNum + yNum)
    mesh.initMesh0(nv, nt, nb)
    idx = 0
    for i in range(yNum + 1):
        for j in range(xNum + 1):
            mesh.nodes[idx] = [(j+0.0)*xLength/xNum, (i + 0.0)*yWide / yNum]
            idx += 1
    createRectangleElements(mesh, xNum, yNum)
    createRectangleBoundarys(mesh, xNum, yNum)
    return mesh


def createRectangleElements(mesh, xNum, yNum):
    ti1 = 0
    tj1 = 0
    tk1 = 0
    ti2 = 0
    tj2 = 0
    tk2 = 0
    idx = 0
    for i in range(yNum):
        for j in range(xNum):
            ti1 = i *(xNum+1) + j
            tj1=ti1+1
            tk1=tj1+xNum+1
            tj2=tk1
            tk2=tj2-1
            ti2=ti1
            mesh.elements[idx] = [ti1, tj1, tk1]
            idx += 1
            mesh.elements[idx] = [ti2, tj2, tk2]
            idx += 1



def createRectangleBoundarys(mesh, xNum, yNum):
    idx = 0
    for i in range(xNum):
        mesh.boundaries[idx], mesh.boundaryLabel[idx] = [i, i + 1], 1
        idx += 1
    for i in range(yNum):
        local = xNum + i * (xNum + 1)
        mesh.boundaries[idx], mesh.boundaryLabel[idx] = [local, local + xNum + 1], 2
        idx += 1
    for i in range(xNum):
        local = (xNum+1)*(yNum+1) - 1 - i
        mesh.boundaries[idx], mesh.boundaryLabel[idx] = [local, local - 1], 3
        idx += 1
    for i in range(yNum):
        local = (yNum - i) * (xNum + 1)
        mesh.boundaries[idx], mesh.boundaryLabel[idx] = [local, local - (xNum + 1)], 4
        idx += 1




mesh=rectangle2D(10,10,1,1)
'''print("Nodes:")
mesh.printNodes()
print("Elements:")
mesh.printElements()
print("Boundaries:")
mesh.printBoundaries()
mesh.plotMesh()'''

f =lambda x,y : np.exp(x+y)
#f =lambda x,y : pow(x,2)*y
def areaK(xy):#xy为存储三角形顶点的数组,按逆时针存储
    S=0
    S=xy[1,0]*xy[2,1]-xy[2,0]*xy[1,1]-xy[0,0]*xy[2,1]+xy[2,0]*xy[0,1]+xy[0,0]*xy[1,1]-xy[1,0]*xy[0,1]
    S=S/2
    return S

nt=mesh.nt
value1=0
for i in range (nt):
    ele = mesh.elements[i, :]
    xy = mesh.nodes[ele, :]
    Ki = areaK(xy)
    for j in range(3):
        value1=value1+(1/6)*Ki*pow(f(xy[j,0],xy[j,1]),2)
    value1=value1+(1/6)*Ki*(f(xy[0,0],xy[0,1])*(f(xy[1,0],xy[1,1])+f(xy[2,0],xy[2,1]))+f(xy[1,0],xy[1,1])*f(xy[2,0],xy[2,1]))
print("法1：",value1)

value2=0
for i in range (nt):
    ele=mesh.elements[i,:]
    xy=mesh.nodes[ele,:]
    Ki=areaK(xy)
    for j in range(3):
        value2=value2+(1/3)*Ki*f(xy[j,0],xy[j,1])*f(xy[j,0],xy[j,1])
print("法2：",value2)




