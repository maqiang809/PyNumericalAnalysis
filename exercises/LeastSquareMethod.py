import numpy as np
import matplotlib.pyplot as plt
#最小二乘法函数
def leastSquare(x, y):
    if len(x) == 2:
        sx = 0.5 * (x[1] - x[0] + 1) * (x[1] + x[0])
        ex = sx / (x[1] - x[0] + 1)
        sx2 = ((x[1] * (x[1] + 1) * (2 * x[1] + 1))
               - (x[0] * (x[0] - 1) * (2 * x[0] - 1))) / 6
        x = np.array(range(x[0], x[1] + 1))
    else:
        sx = sum(x)
        ex = sx / len(x)
        sx2 = sum(x ** 2)

    sxy = sum(x * y)
    ey = np.mean(y)

    a = (sxy - ey * sx) / (sx2 - ex * sx)
    b = (ey * sx2 - sxy * ex) / (sx2 - ex * sx)
    return a, b
#测试
x = np.arange(25)            #arange函数返回array对象，range返回一个list对象，起始值为start，终止值为end，但不含终止值，步长为step。只能创建int型list。
y = x*15+20+np.random.randn(len(x))*5  ##randn生成正态分布噪声
a,b = leastSquare(x,y)
#print(x)
#print(y)
plt.scatter(x,y)
plt.plot(x,a*x+b)
plt.show()