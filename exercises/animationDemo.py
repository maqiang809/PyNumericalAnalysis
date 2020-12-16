import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 建立一个画板
fig = plt.figure()
# 把画板分成1x1的栅格，并使用1号格子
# ax = fig.add_subplot(2,2,4)分成2x2的栅格，使用4号格子
ax = fig.add_subplot(1, 1, 1)
x = np.linspace(0, 5, 20)
# 在ax的对象上建立'两条线',根据需要可以命名，因为需要让line1动起来，所以给他命名了
xdata, ydata = [], []
line1, = ax.plot([], [])

ax.plot(x, x ** 3)


# 根据对象的所有点的坐标，依次连接成线

def init():
    global xdata, ydata
    del xdata[:]
    del ydata[:]


def data_gen():
    global x
    for i in x:
        yield i, i ** 2


def update(xy_pos):
    global xdata, ydata
    xpos, ypos = xy_pos
    xdata.append(xpos)
    ydata.append(ypos)
    line1.set_data(xdata, ydata)


anima = animation.FuncAnimation(fig, update, data_gen, blit=False, interval=3, repeat=False, init_func=init)
plt.show()