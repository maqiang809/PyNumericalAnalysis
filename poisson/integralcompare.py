import numpy as np
from mesh.MeshGenerator import square2D
import matplotlib.pyplot as plt

n = 100
mesh = square2D(n, n, 1)
# mesh.plotMesh()
# mesh.scale(4.0, 4.0)
# mesh.plotMesh()
nodes = mesh.nodes
elements = mesh.elements
boundaries = mesh.boundaries

def area3(x, y):
    S = 0
    for i in range(2):
        S = S + x[i] * y[i + 1] - x[i + 1] * y[i]
    S = S + x[2] * y[0] - x[0] * y[2]
    S = S / 2
    return S

def I1(fun, c):
    I1 = 0
    for i in range(c):
        ff = 0
        x = np.zeros(3)
        y = np.zeros(3)
        for j in range(3):
            xx = nodes[elements[i, j]]
            x[j] = xx[0]
            y[j] = xx[1]
            ff += f(xx[0], xx[1])
        K = area3(x, y)
        I1 += (1 / 6) * K * ff ** 2
    print(I1)


def I2(fun,c):
    I2 = 0
    for i in range(c):
        x = np.zeros(3)
        y = np.zeros(3)
        h = 0
        for j in range(3):
            xx = nodes[elements[i, j]]
            x[j] = xx[0]
            y[j] = xx[1]
            h += f(xx[0], xx[1]) ** 2
        K = area3(x, y)
        I2 += h * K * (1/3)
    print(I2)


c = (n+1) * (n+1)


def f(x, y):
    return x + y

print("x + y的积分比较")
I1(f, c)
I2(f, c)
def f(x, y):
    return x * y

print("x * y的积分比较")
I1(f, c)
I2(f, c)
def f(x, y):
    return (x + y) ** 2

print("(x + y) ** 2的积分比较")
I1(f, c)
I2(f, c)
def f(x, y):
    return x ** y

print("x ** y的积分比较")
I1(f, c)
I2(f, c)
def f(x, y):
    return x / (1+y)

print("x / (1+y)的积分比较")
I1(f, c)
I2(f, c)