import numpy as np
def getCoefFromFunc(coefFunc, coord, label, param, coef):
    row, col = coef.shape
    for i in range(row):
        for j in range(col):
            coef[i][j] = coefFunc[i](coord[j, :], label, param)

def getDof(ele, dofPerNode):
    n = len(ele)
    dof = np.zeros(n * dofPerNode, dtype=np.int32)
    for i in range(n):
        start = ele[i] * dofPerNode
        startIdx = i * dofPerNode
        for j in range(dofPerNode):
            dof[j + startIdx] = start + j
    return dof

class FES:
    def __init__(self, mesh, dofPerNode):
        self.mesh = mesh
        self.nDim = mesh.Dim
        self.dofPerNode = dofPerNode
        self.nDof = dofPerNode * mesh.NumberOfNodes

        self.nE = mesh.NumberOfElements
        self.nPerEle = mesh.NumberPerElement
        self.dofPerElement = dofPerNode * mesh.NumberPerElement

        self.nB = mesh.NumberOfBoundaries
        self.nPerBoundary = mesh.NumberPerBoundary
        self.dofPerBoundary = dofPerNode * mesh.NumberPerBoundary


    def assembleGlobalMatrix_Func(self, coeffFunc, param, EleMatFunc, BVPType, A):
        coef = np.zeros((len(coeffFunc), self.nPerEle), dtype=np.float)
        eleMatrix = np.zeros((self.dofPerElement, self.dofPerElement), dtype = np.float)
        for i in range(self.nE):
            ele = self.mesh.getElement(i)
            coord = self.mesh.getCoordInElement(ele)
            getCoefFromFunc(coeffFunc, coord, self.mesh.getElementLabel(i), param, coef)
            EleMatFunc(coord, coef, BVPType, eleMatrix)
            dof = getDof(ele, self.dofPerNode)
            A.assemble_RC(dof, dof, eleMatrix)

    def assembleGlobalMatrix_Const(self, constCoef, EleMatFunc, BVPType, A):
        nc = len(constCoef)
        coef = np.zeros((nc, self.nPerEle), dtype=np.float)
        eleMatrix = np.zeros((self.dofPerElement, self.dofPerElement), dtype = np.float)
        for i in range(self.nE):
            ele = self.mesh.getElement(i)
            coord = self.mesh.getCoordInElement(ele)
            for j in range(nc):
                coef[j, :] = constCoef[j]
            EleMatFunc(coord, coef, BVPType, eleMatrix)
            dof = getDof(ele, self.dofPerNode)
            A.assemble_RC(dof, dof, eleMatrix)

    def assembleGlobalVector_Const(self, constCoef, EleVecFunc, BVPType, VEC):
        nc = len(constCoef)
        coef = np.zeros((nc, self.nPerEle), dtype=np.float)
        eleVec = np.zeros(self.dofPerElement, dtype = np.float)
        for i in range(self.nE):
            ele = self.mesh.getElement(i)
            coord = self.mesh.getCoordInElement(ele)
            for j in range(nc):
                coef[j, :] = constCoef[j]
            EleVecFunc(coord, coef, BVPType, eleVec)
            dof = getDof(ele, self.dofPerNode)
            VEC[dof] += eleVec