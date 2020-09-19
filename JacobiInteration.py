import numpy as np

def Jacobi(A, b, x0, esp):
    A = np.array(A, dtype=float)#dtype=float定义数组类型为浮点型
    (m, n) = np.shape(A)#shape()获取矩阵的行列数
    D = np.zeros((m, n))#zero()生成m×n阶的元素全为0的矩阵
    for i in range(m):
        D[i,i]=A[i,i]#取D为A的对角元素矩阵
    if np.linalg.det(D) ==0.0:
        print("Jacobi cannot be used!Please input again.")
    else:
        B=-np.dot(np.linalg.inv(D),A-D)#得迭代矩阵B；dot()矩阵乘法
        eigvals=np.linalg.eigvals(B)#求矩阵B得特征值
        pB=np.max(np.abs(eigvals))#求矩阵B得谱半径
        if pB<1.0:#Convergence of Jacobi Interation 当且仅当 迭代矩阵B的谱半径小于1
            f = np.dot(np.linalg.inv(D), b)
            t=np.dot(B,x0)+f
            x=x0
            iter=1#记录迭代次数
            while np.linalg.norm(t-x,ord=2)>esp:#利用二范数<esp来作为迭代终止条件
                x=t
                t=np.dot(B,x)+f#Jacobi迭代公式
                iter=iter+1
            print("The number of interation is ",iter)
            print("近似解为：",t)
        else:
            print("Jacobi diverges")

A1=np.array([[5,1,-1,-2],
             [2,8,1,3],
             [1,-2,-4,-1],
             [-1,3,2,7]])
b1=np.array([[-2],
             [-6],
             [6],
             [12]])
X0=([[0],[0],[0],[0]])
esp=1e-5
Jacobi(A1, b1, X0, esp)

A2=([[2,9],
     [8,3]])
b2=([[-5],
     [13]])
x0=([0],
    [0])
Jacobi(A2, b2, x0, esp)