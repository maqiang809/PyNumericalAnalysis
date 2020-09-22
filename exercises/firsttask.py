import numpy as np

a = np.array([[1, 1, -2, -1, 4], [3, -2, -3, 2, 2], [0, 5, 7, 3, -2], [2, -3, -5, -1, 4]])
b = np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
for i in range(4):
    h = 0
    m = a[0, 0]
    for j in range(3 - i):
        if m < a[j + 1, i]:
            h = j + 1
            m = a[j + 1, i]
    b[i] = a[h] / a[h,i]
    print(b[i])
    a = np.delete(a, h, axis=0)
    for t in range(3 - i):
        a[t] = a[t] - a[t, i] * b[i]

for i in range(3):
    for j in range(i + 1):
        b[j] = b[j] - b[j, i + 1] * b[i + 1]
    print(b)
