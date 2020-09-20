import numpy as np
def getCoefFromFunc(coefFunc, coord, label, param, coef):
    row, col = coef.shape
    for i in range(row):
        for j in range(col):
            coef[i, j] = coefFunc[i](coord[j, :], label, param)

def getDof(ele, dofPerNode):
    return np.tile(np.arange(dofPerNode), len(ele))  + np.repeat(ele * dofPerNode, dofPerNode)

DIRECT = {"x":0, "y":1, "z":2, "all":-1}

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

    def assembleBlobalMatrix(self, coef, param, EleMatFunc, tp, A):
        if callable(coef):
            self.assembleGlobalMatrix_Func(coef, param, EleMatFunc, tp, A)
        elif isinstance(coef, np.ndarray):
            ndim = coef.ndim
            if ndim == 1:
                self.assembleGlobalMatrix_Const(coef, EleMatFunc, tp, A)
            elif ndim == 2:
                self.assembleGlobalMatrix_Vector(coef, EleMatFunc, tp, A)
            elif ndim == 3:
                self.assembleGlobalMatrix_Matrix(coef, EleMatFunc, tp, A)
        else:
            raise ValueError("Wrong coef Type!")

    def assembleGlobalMatrix_Func(self, coeffFunc, param, EleMatFunc, tp, A):
        coef = np.zeros((len(coeffFunc), self.nPerEle), dtype=np.float)
        eleMatrix = np.zeros((self.dofPerElement, self.dofPerElement), dtype = np.float)
        for i in range(self.nE):
            ele = self.mesh.getElement(i)
            coord = self.mesh.getCoordFromIdx(ele)
            getCoefFromFunc(coeffFunc, coord, self.mesh.getElementLabel(i), param, coef)
            EleMatFunc(coord, coef, tp, eleMatrix)
            dof = getDof(ele, self.dofPerNode)
            A.assemble_RC(dof, dof, eleMatrix)

    def assembleGlobalMatrix_Const(self, constCoef, EleMatFunc, BVPType, A):
        nc = len(constCoef)
        coef = np.zeros((nc, self.nPerEle), dtype=np.float)
        eleMatrix = np.zeros((self.dofPerElement, self.dofPerElement), dtype = np.float)
        for i in range(self.nE):
            ele = self.mesh.getElement(i)
            coord = self.mesh.getCoordFromIdx(ele)
            for j in range(nc):
                coef[j, :] = constCoef[j]
            EleMatFunc(coord, coef, BVPType, eleMatrix)
            dof = getDof(ele, self.dofPerNode)
            A.assemble_RC(dof, dof, eleMatrix)

    def assembleGlobalMatrix_Vector(self, vecCoef, EleMatFunc, BVPType, A):
        nc = vecCoef.shape[0]
        coef = np.zeros((nc, self.nPerEle), dtype=np.float)
        eleMatrix = np.zeros((self.dofPerElement, self.dofPerElement), dtype = np.float)
        for i in range(self.nE):
            ele = self.mesh.getElement(i)
            coord = self.mesh.getCoordFromIdx(ele)
            for j in range(nc):
                coef[j, :] = vecCoef[j, ele]
            EleMatFunc(coord, coef, BVPType, eleMatrix)
            dof = getDof(ele, self.dofPerNode)
            A.assemble_RC(dof, dof, eleMatrix)

    def assembleGlobalMatrix_Matrix(self, matrixCoef, EleMatFunc, BVPType, A):
        eleMatrix = np.zeros((self.dofPerElement, self.dofPerElement), dtype = np.float)
        for i in range(self.nE):
            ele = self.mesh.getElement(i)
            coord = self.mesh.getCoordFromIdx(ele)
            EleMatFunc(coord, matrixCoef, BVPType, eleMatrix)
            dof = getDof(ele, self.dofPerNode)
            A.assemble_RC(dof, dof, eleMatrix)

    def assembleGlobalVector_Func(self, FuncCoef, param, EleVecFunc, BVPType, VEC):
        nc = len(FuncCoef)
        coef = np.zeros((nc, self.nPerEle), dtype=np.float)
        eleVec = np.zeros(self.dofPerElement, dtype = np.float)
        for i in range(self.nE):
            ele = self.mesh.getElement(i)
            coord = self.mesh.getCoordFromIdx(ele)
            getCoefFromFunc(FuncCoef, coord, self.mesh.getElementLabel(i), param, coef)
            EleVecFunc(coord, coef, BVPType, eleVec)
            dof = getDof(ele, self.dofPerNode)
            VEC[dof] += eleVec


    def assembleGlobalVector_Const(self, constCoef, EleVecFunc, BVPType, VEC):
        nc = len(constCoef)
        coef = np.zeros((nc, self.nPerEle), dtype=np.float)
        eleVec = np.zeros(self.dofPerElement, dtype = np.float)
        for i in range(self.nE):
            ele = self.mesh.getElement(i)
            coord = self.mesh.getCoordFromIdx(ele)
            for j in range(nc):
                coef[j, :] = constCoef[j]
            EleVecFunc(coord, coef, BVPType, eleVec)
            dof = getDof(ele, self.dofPerNode)
            VEC[dof] += eleVec

    def applyBC_MBN_MR(self, A, RHS, direct=None, bdValue=None, param=None, label=None):
        bdNodes = self.mesh.getBoundariesNodes(label)
        if direct is None:
            for nodeIdx in bdNodes:
                coord = self.mesh.getCoordFromIdx(nodeIdx)
                value = 0
                if bdValue is not None:
                    if callable(bdValue):
                        value = bdValue(coord, self.mesh.getNodeLabel[nodeIdx], param)
                    else:
                        value = bdValue
                localIdx = np.arange(self.dofPerNode) + nodeIdx * self.dofPerNode
                for idx in localIdx:
                    A.setElement(localIdx, localIdx, 1.0e30)
                RHS[localIdx] = value * 1.0e30
        else:
            offset = DIRECT[direct]
            for nodeIdx in bdNodes:
                coord = self.mesh.getCoordFromIdx(nodeIdx)
                value = 0
                if bdValue is not None:
                    if callable(bdValue):
                        value = bdValue(coord, self.mesh.getNodeLabel[nodeIdx], param)
                    else:
                        value = bdValue
                localIdx = nodeIdx * self.dofPerNode + offset
                A.setElement(localIdx, localIdx, 1.0e30)
                RHS[localIdx] = value * 1.0e30

    def applyBC_MBN_R(self, RHS, direct=None, bdValue=None, param=None, label=None):
        bdNodes = self.mesh.getBoundariesNodes(label)
        if direct is None:
            for nodeIdx in bdNodes:
                coord = self.mesh.getCoordFromIdx(nodeIdx)
                value = 0
                if bdValue is not None:
                    if callable(bdValue):
                        value = bdValue(coord, self.mesh.getNodeLabel[nodeIdx], param)
                    else:
                        value = bdValue
                RHS[np.arange(self.dofPerNode) + nodeIdx * self.dofPerNode] = value * 1.0e30
        else:
            offset = DIRECT[direct]
            for nodeIdx in bdNodes:
                coord = self.mesh.getCoordFromIdx(nodeIdx)
                value = 0
                if bdValue is not None:
                    if callable(bdValue):
                        value = bdValue(coord, self.mesh.getNodeLabel[nodeIdx], param)
                    else:
                        value = bdValue
                RHS[nodeIdx * self.dofPerNode + offset] = value * 1.0e30

    def applyBC_MBN_M(self, A, direct=None, bdValue=None, param=None, label=None):
        bdNodes = self.mesh.getBoundariesNodes(label)
        if direct is None:
            for nodeIdx in bdNodes:
                coord = self.mesh.getCoordFromIdx(nodeIdx)
                value = 0
                if bdValue is not None:
                    if callable(bdValue):
                        value = bdValue(coord, self.mesh.getNodeLabel[nodeIdx], param)
                    else:
                        value = bdValue
                localIdx = np.arange(self.dofPerNode) + nodeIdx * self.dofPerNode
                for idx in localIdx:
                    A.setElement(localIdx, localIdx, 1.0e30)
        else:
            offset = DIRECT[direct]
            for nodeIdx in bdNodes:
                coord = self.mesh.getCoordFromIdx(nodeIdx)
                value = 0
                if bdValue is not None:
                    if callable(bdValue):
                        value = bdValue(coord, self.mesh.getNodeLabel[nodeIdx], param)
                    else:
                        value = bdValue
                localIdx = nodeIdx * self.dofPerNode + offset
                A.setElement(localIdx, localIdx, 1.0e30)
