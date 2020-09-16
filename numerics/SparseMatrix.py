import numpy as np
from scipy import sparse
from numerics.ParamCheck import checkEqual
'''
sparse matrix
'''
class SMatrix:
    def __init__(self, **params):  # 设置稀疏矩阵的维数
        paramLen = len(params)
        if paramLen == 2:
            m, n = params['row'], params['col']
            self.m, self.n = m, n
            self.mat = [None] * m
            for i in range(m):
                self.mat[i] = []
        elif paramLen == 1:
            n = params['size']
            m = n
            self.m, self.n = n, n
            self.mat = [None] * m
            for i in range(m):
                self.mat[i] = []
        elif paramLen == 5:
            m, n = params['row'], params['col']
            rowIdx, colIdx, values = params['rowIdx'], params['colIdx'], params['values']
            self.m, self.n = m, n
            self.mat = [None] * m
            for i in range(m):
                self.mat[i] = []
            nnz = len(rowIdx)
            for i in range(nnz):
                self.mat[rowIdx[i]].append(colIdx[i], values[i])
        else:
            raise ValueError("Param Error!")

    def setElement(self, i, j, val):
        """ 设置(i,j)的元素值，如果输入了零值，需删除
        Args:
            i: 矩阵行指标
            j: 矩阵列指标
            val: 要设置的值
        Returns:
        Raises:
            ValueError: 如果行指标与列指标超过矩阵行列指标范围, 则报错
        """
        row = self.mat[i]
        nRow = len(self.mat[i])
        for k in range(nRow):
            if row[k][0] == j:
                if np.abs(val) < 1.0e-10:  # 实数比较，如果这个数字充分小，默认为0
                    del row[k]
                    return
                else:
                    row[k][1] = val
                    return
        if np.abs(val) > 1.0e-10:
            self.mat[i].append([j, val])

    def getElement(self, i, j):  # 取得(i,j)的元素值
        for ele in self.mat[i]:
            if ele[0] == j:
                return ele[1]
        return 0.0

    def addElement(self, i, j, val):
        row = self.mat[i]
        nRow = len(self.mat[i])
        if np.abs(val) > 1.0e-10:
            for k in range(nRow):
                if row[k][0] == j:
                    if np.abs(val + row[k][1]) < 1.0e-10:  # 实数比较，如果这个数字充分小，默认为0
                        del row[k]
                    else:
                        row[k][1] += val
                    return
        if np.abs(val) > 1.0e-10:
            self.mat[i].append([j, val])

    def assemble_ROW(self, row, colDof, ele):
        m = len(ele)
        checkEqual(m, len(colDof))
        for i in range(m):
            self.addElement(row, colDof[i], ele[i])

    def assemble_COL(self, rowDof, col, ele):
        m = len(ele)
        checkEqual(m, len(rowDof))
        for i in range(m):
            self.addElement(rowDof[i], col, ele[i])

    def assemble_RC(self, rowDof, colDof, mat):
        m, n = mat.shape
        checkEqual(m, len(rowDof))
        checkEqual(n, len(colDof))
        for i in range(m):
            for j in range(n):
                self.addElement(rowDof[i], colDof[j], mat[i][j])

    def sort(self):
        for i in range(self.m):
            self.mat[i].sort(key=lambda ele:ele[0])

    def printMatrix(self):  # 打印矩阵
        nnz = self.getNNZ()
        print(self.m, self.n, nnz)
        for i in range(self.m):
            for ele in self.mat[i]:
                print("%-8d%-8d%.10f" % (i, ele[0], ele[1]))

    def getNNZ(self):  # 获得非零元总数
        count = 0
        for i in range(self.m):
            count += len(self.mat[i])
        return count

    def exportTriple(self):  # 返回行、列、值三元数组
        row = []
        col = []
        data = []
        for i in range(self.m):
            for ele in self.mat[i]:
                row.append(i)
                col.append(ele[0])
                data.append(ele[1])
        return row, col, data

    def toCSR_Matrix(self):  # 转化为csr格式，方便进行矩阵运算
        row, col, data = self.exportTriple()
        return sparse.csr_matrix((data, (row, col)), shape=(self.m, self.n))

    def toCSC_Matrix(self):
        row, col, data = self.exportTriple()
        return sparse.csc_matrix((data, (row, col)), shape=(self.m, self.n))

    def copy(self):
        result = SMatrix(self.m, self.n)
        for i in range(self.m):
            for ele in self.mat[i]:
                result.mat[i].append([ele[0], ele[1]])
        return result

    def __add__(self, matB):
        result = self.copy()
        m = matB.m
        flag = 0
        for i in range(m):
            for ele in matB.mat[i]:
                flag = 0
                for eleA in result.mat[i]:
                    if eleA[0] == ele[0]:
                        flag = 1
                        temp = eleA[1] + ele[1]
                        if np.abs(temp) < 1.0e-10:
                            result.mat[i].remove([eleA[0], eleA[1]])
                        else:
                            eleA[1] = temp
                        break
                if flag == 0:
                    result.mat[i].append([ele[0], ele[1]])
        return result

    def __sub__(self, matB):
        result = self.copy()
        m = matB.m
        flag = 0
        for i in range(m):
            for ele in matB.mat[i]:
                flag = 0
                for eleA in result.mat[i]:
                    if eleA[0] == ele[0]:
                        flag = 1
                        temp = eleA[1] - ele[1]
                        if np.abs(temp) < 1.0e-10:
                            result.mat[i].remove([eleA[0], eleA[1]])
                        else:
                            eleA[1] = temp
                        break
                if flag == 0:
                    result.mat[i].append([ele[0], -ele[1]])
        return result

    def __mul__(self, var):
        if type(var) == float:
            result = SMatrix(self.m, self.n)
            for i in range(self.m):
                for ele in self.mat[i]:
                    result.mat[i].append([ele[0], ele[1] * var])
            return result
        elif type(var) == np.ndarray:  # 矩阵右乘列向量，返还一个列向量
            result = np.zeros(self.m)
            if len(var) == self.n:
                for i in range(self.m):
                    for ele in self.mat[i]:
                        result[i] = result[i] + var[ele[0]] * ele[1]
                return result
            else:
                print('wrong')

    def mul(self, vec):
        result = np.zeros(self.m)
        if len(vec) == self.n:
            for i in range(self.m):
                for ele in self.mat[i]:
                    result[i] = result[i] + vec[ele[0]] * ele[1]
        else:
            print('wrong!')
        return result

# A.printMatrix()
A = SMatrix(row=5, col=5)
A.printMatrix()
for i in range(3):
    for j in range(3):
        A.setElement(i, j, 1.0/(i + j + 1))
A.setElement(4, 4, 2.0)
A.setElement(4, 2, 3.5)
A.printMatrix()
A.sort()
print("sorted matrix")
A.printMatrix()

