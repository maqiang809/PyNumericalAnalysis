import numpy as np
import abc
class AMesh:
    def __init__(self):
        self.nv = 0
        self.nt = 0
        self.nb = 0
        self.nDim = 0
        self.nPerElement = 0
        self.nPerBoundary = 0
        self.nBoundaryPerElement = 0
        self.nEdgePerElement = 0
        self.nEdgePerBoundary = 0
        self.tecplotType = ""
        self.nodes = None
        self.nodeLabel = None
        self.elements = None
        self.elementLabel = None
        self.boundaries = None
        self.boundaryLabel = None
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
    @property
    def Dim(self):
        return self.nDim

    @property
    def NumberOfNodes(self):
        return self.nv

    @property
    def NumberOfElements(self):
        return self.nt

    @property
    def NumberPerElement(self):
        return self.nPerElement

    @property
    def NumberOfBoundaries(self):
        return self.nb

    @property
    def NumberPerBoundary(self):
        return self.nPerBoundary

    def getNodeLabel(self, i):
        return self.nodeLabel[i]

    def getElement(self, i):
        return self.elements[i]

    def getElementLabel(self, i):
        return self.elementLabel[i]

    def getElement(self, i):
        return self.elements[i].copy()

    def getBoundary(self, i):
        return self.boundaries[i].copy()

    def getBoundaryLabel(self, i):
        return self.boundaryLabel[i]

    def getCoordFromIdx(self, idx):
        return self.nodes[idx, :]

    def getInteriorPointInElement(self, coord):
        return coord.mean(axis=1)

    def getBoundariesNodes(self, label):      # 已知边界label 求出该边界上所有的节点\
        if label is None:
            return np.unique(self.boundaries.flatten())
        else:
            bdNodes = []
            for i in range(self.nb):
                ele = self.boundaries[i, :]
                if self.boundaryLabel[i] in label:
                    bdNodes.extend(ele)
        return np.unique(bdNodes)     # unique方法能删除列表的重复元素 并从小到大排序

    def saveMesh(self, fileName):
        f = open(fileName, 'w')
        f.write(str(self.nv) + ' ' + str(self.nt) + ' ' + str(self.nb) + '\n')
        for i in range(self.nv):
            for j in range(self.nDim):
                f.write("%.16f" % self.nodes[i, j] + "\t ")
            f.write(str(self.nodeLabel[i]) + "\n")
        for i in range(self.nt):
            for j in range(self.nPerElement):
                f.write(str(self.elements[i, j] + 1) + "\t ")
            f.write(str(self.elementLabel[i]) + "\n")
        for i in range(self.nb):
            for j in range(self.nPerBoundary):
                f.write(str(self.boundaries[i, j] + 1) + "\t ")
            f.write(str(self.boundaryLabel[i]) + "\n")
        f.close()

    def meshfunc(self, func):
        u = np.zeros(self.nv)
        for i in range(self.nv):
            u[i] = func(self.nodes[i, :])
        return u

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