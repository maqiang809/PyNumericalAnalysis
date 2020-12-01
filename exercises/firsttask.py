import numpy as np

def xiaoyuan(a):
    n = np.shape(a)[0]
    for i in range(n):
        h = 0
        m = a[0, 0]
        for j in range(n - 1 - i):
            if m < a[j + 1, i]:
                h = j + 1
                m = a[h, i]
        b[i] = a[h] / a[h, i]
        a = np.delete(a, h, axis=0)
        for t in range(n - 1 - i):
            a[t] = a[t] - a[t, i] * b[i]

    for i in range(n - 1):
        for j in range(i + 1):
            b[j] = b[j] - b[j, i + 1] * b[i + 1]
    print(b)


a = np.array([[2.0, 3.0, 11.0, 5.0, 2.0],
              [1.0, 1.0, 5.0, 2.0, 1.0],
              [2.0, 1.0, 3.0, 2.0, -3.0],
              [1.0, 1.0, 3.0, 3.0, -3.0]])
b = np.array([[0.0, 0.0, 0.0, 0.0, 0.0],
              [0.0, 0.0, 0.0, 0.0, 0.0],
              [0.0, 0.0, 0.0, 0.0, 0.0],
              [0.0, 0.0, 0.0, 0.0, 0.0]])
xiaoyuan(a)
