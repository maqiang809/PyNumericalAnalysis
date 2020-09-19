import numpy as np
a=np.array([[1,1,-2],[1,-1,4],[2,0,3]])#系数矩阵
b=np.array([5,-2,2.5])
x=np.linalg.solve(a,b)#linalg线性代数模板，利用自带的solve函数求解线性方程组
print(x)