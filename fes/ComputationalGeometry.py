import numpy as np

def length2DL2(xy):
    return np.sqrt((xy[0][0] - xy[1][0]) * (xy[0][0] - xy[1][0]) + (xy[0][1] - xy[1][1]) * (xy[0][1] - xy[1][1]))

def area2DT3(xy):
    x, y = xy[:, 0], xy[:, 1]
    return 0.5 * ((x[1] - x[0]) * (y[2] - y[0]) - (x[2] - x[0]) * (y[1] - y[0]))

def area3DT3(xyz):
    x, y, z = xyz[:, 0], xyz[:, 1], xyz[:, 2]
    a = np.sqrt((x[0] - x[1]) * (x[0] - x[1]) + (y[0] - y[1]) * (y[0] - y[1]) + (z[0] - z[1]) * (z[0] - z[1]))
    b = np.sqrt((x[1] - x[2]) * (x[1] - x[2]) + (y[1] - y[2]) * (y[1] - y[2]) + (z[1] - z[2]) * (z[1] - z[2]))
    c = np.sqrt((x[2] - x[0]) * (x[2] - x[0]) + (y[2] - y[0]) * (y[2] - y[0]) + (z[2] - z[0]) * (z[2] - z[0]))
    p = 0.5 * (a + b + c)
    return np.sqrt(p * (p - a) * (p - b) * (p - c));

def area2DQ4(xy):
    xy1, xy2 = xy[[0, 1, 2]][:], xy[[0, 2, 3]][:]
    return area2DT3(xy1) + area2DT3(xy2)

def area3DQ4(xyz):
    xyz1, xyz2 = xyz[[0, 1, 2]][:], xyz[[0, 2, 3]][:]
    return area3DT3(xyz1) + area3DT3(xyz2)

def volume3DT4(coord):
    x, y, z= coord[:, 0], coord[:, 1], coord[:, 2]
    x1x0 = x[1] - x[0]
    x2x0 = x[2] - x[0]
    x3x0 = x[3] - x[0]
    y1y0 = y[1] - y[0]
    y2y0 = y[2] - y[0]
    y3y0 = y[3] - y[0]
    z1z0 = z[1] - z[0]
    z2z0 = z[2] - z[0]
    z3z0 = z[3] - z[0]
    volume6 = x1x0 * (y2y0 * z3z0 - y3y0 * z2z0) - x2x0 * (y1y0 * z3z0 - y3y0 * z1z0) \
                + x3x0 * (y1y0 * z2z0 - y2y0 * z1z0)
    return np.abs(volume6) / 6.0

def volume3DTH8(xyz):
    pass

def gradient1DL2(coord):
    x = coord[:, 0]
    len = np.abs(x[0] - x[1])
    grad = np.array([-1.0/len, 1.0/len])
    return grad, len

def gradient2DT3(coord):
    x, y = coord[:, 0], coord[:, 1]
    area = 0.5 * ((x[1] - x[0]) * (y[2] - y[0]) - (x[2] - x[0]) * (y[1] - y[0]))
    A2D = 1 / (2 * area)
    grad = np.zeros((3, 2))
    grad[0][0] = A2D * (y[1] - y[2])
    grad[1][0] = A2D * (y[2] - y[0])
    grad[2][0] = A2D * (y[0] - y[1])
    grad[0][1] = A2D * (x[2] - x[1])
    grad[1][1] = A2D * (x[0] - x[2])
    grad[2][1] = A2D * (x[1] - x[0])
    return grad, area

def gradient3DT4(coord):
    x, y, z = coord[:, 0], coord[:, 1], coord[:, 2]
    x1x0 = x[1] - x[0]
    x2x0 = x[2] - x[0]
    x3x0 = x[3] - x[0]
    x2x1 = x[2] - x[1]
    x3x1 = x[3] - x[1]
    y1y0 = y[1] - y[0]
    y2y0 = y[2] - y[0]
    y3y0 = y[3] - y[0]
    y2y1 = y[2] - y[1]
    y3y1 = y[3] - y[1]
    z1z0 = z[1] - z[0]
    z2z0 = z[2] - z[0]
    z3z0 = z[3] - z[0]
    z2z1 = z[2] - z[1]
    z3z1 = z[3] - z[1]

    volume6 = x1x0 * (y2y0 * z3z0 - y3y0 * z2z0) - x2x0 * (y1y0 * z3z0 - y3y0 * z1z0) + x3x0 * (y1y0 * z2z0 - y2y0 * z1z0)
    grad = np.zeros(4, 3)
    grad[0][0] = -(y2y1 * z3z1 - y3y1 * z2z1) / volume6
    grad[0][1] = +(x2x1 * z3z1 - x3x1 * z2z1) / volume6
    grad[0][2] = -(x2x1 * y3y1 - x3x1 * y2y1) / volume6
    grad[1][0] = +(y2y0 * z3z0 - y3y0 * z2z0) / volume6
    grad[1][1] = -(x2x0 * z3z0 - x3x0 * z2z0) / volume6
    grad[1][2] = +(x2x0 * y3y0 - x3x0 * y2y0) / volume6
    grad[2][0] = -(y1y0 * z3z0 - y3y0 * z1z0) / volume6
    grad[2][1] = +(x1x0 * z3z0 - x3x0 * z1z0) / volume6
    grad[2][2] = -(x1x0 * y3y0 - x3x0 * y1y0) / volume6
    grad[3][0] = +(y1y0 * z2z0 - y2y0 * z1z0) / volume6
    grad[3][1] = -(x1x0 * z2z0 - x2x0 * z1z0) / volume6
    grad[3][2] = +(x1x0 * y2y0 - x2x0 * y1y0) / volume6

    return grad, np.abs(volume6 / 6)


def Q4ShapeFunction(xi, et, h, dXi, dEt):
    h[0] = 0.25 * (1 - xi) * (1 - et)
    h[1] = 0.25 * (1 + xi) * (1 - et)
    h[2] = 0.25 * (1 + xi) * (1 + et)
    h[3] = 0.25 * (1 - xi) * (1 + et)

    dXi[0] = 0.25 * (et - 1)
    dXi[1] = 0.25 * (1 - et)
    dXi[2] = 0.25 * (1 + et)
    dXi[3] = 0.25 * (-1 - et)

    dEt[0] = 0.25 * (xi - 1)
    dEt[1] = 0.25 * (-1 - xi)
    dEt[2] = 0.25 * (1 + xi)
    dEt[3] = 0.25 * (1 - xi)

def Q8ShapeFunction(xi, et, h, dXi, dEt):
    h[0] = 0.25 * (1 - xi) * (1 - et) * (-1 - xi - et)
    h[1] = 0.25 * (1 + xi) * (1 - et) * (-1 + xi - et)
    h[2] = 0.25 * (1 + xi) * (1 + et) * (-1 + xi + et)
    h[3] = 0.25 * (1 - xi) * (1 + et) * (-1 - xi + et)
    h[4] = 0.5 * (1 - xi * xi) * (1 - et)
    h[5] = 0.5 * (1 + xi) * (1 - et * et)
    h[6] = 0.5 * (1 - xi * xi) * (1 + et)
    h[7] = 0.5 * (1 - xi) * (1 - et * et)

    dXi[0] = 0.25 * (1 - et) * (2 * xi + et)
    dXi[1] = 0.25 * (1 - et) * (2 * xi - et)
    dXi[2] = 0.25 * (1 + et) * (2 * xi + et)
    dXi[3] = 0.25 * (1 + et) * (2 * xi - et)

    dXi[4] = xi * (et - 1)
    dXi[5] = 0.5 * (1 - et * et)
    dXi[6] = xi * (-et - 1)
    dXi[7] = 0.5 * (-1 + et * et)

    dEt[0] = 0.25 * (1 - xi) * (xi + 2 * et)
    dEt[1] = 0.25 * (1 + xi) * (-xi + 2 * et)
    dEt[2] = 0.25 * (1 + xi) * (xi + 2 * et)
    dEt[3] = 0.25 * (1 - xi) * (-xi + 2 * et)

    dEt[4] = 0.5 * (-1 + xi * xi)
    dEt[5] = et * (-xi - 1)
    dEt[6] = 0.5 * (1 - xi * xi)
    dEt[7] = et * (xi - 1)

def H8ShapeFunction(xi, et, zt, h, dXi, dEt, dZt):
    h[0] = 0.125 * (1 - xi) * (1 - et) * (1 - zt)
    h[1] = 0.125 * (1 + xi) * (1 - et) * (1 - zt)
    h[2] = 0.125 * (1 + xi) * (1 + et) * (1 - zt)
    h[3] = 0.125 * (1 - xi) * (1 + et) * (1 - zt)

    h[4] = 0.125 * (1 - xi) * (1 - et) * (1 + zt)
    h[5] = 0.125 * (1 + xi) * (1 - et) * (1 + zt)
    h[6] = 0.125 * (1 + xi) * (1 + et) * (1 + zt)
    h[7] = 0.125 * (1 - xi) * (1 + et) * (1 + zt)

    dXi[0] = 0.125 * (et - 1) * (1 - zt)
    dXi[1] = 0.125 * (1 - et) * (1 - zt)
    dXi[2] = 0.125 * (1 + et) * (1 - zt)
    dXi[3] = 0.125 * (-1 - et) * (1 - zt)
    dXi[4] = 0.125 * (et - 1) * (1 + zt)
    dXi[5] = 0.125 * (1 - et) * (1 + zt)
    dXi[6] = 0.125 * (1 + et) * (1 + zt)
    dXi[7] = 0.125 * (-1 - et) * (1 + zt)

    dEt[0] = 0.125 * (xi - 1) * (1 - zt)
    dEt[1] = 0.125 * (-1 - xi) * (1 - zt)
    dEt[2] = 0.125 * (1 + xi) * (1 - zt)
    dEt[3] = 0.125 * (1 - xi) * (1 - zt)
    dEt[4] = 0.125 * (xi - 1) * (1 + zt)
    dEt[5] = 0.125 * (-1 - xi) * (1 + zt)
    dEt[6] = 0.125 * (1 + xi) * (1 + zt)
    dEt[7] = 0.125 * (1 - xi) * (1 + zt)

    dZt[0] = -0.125 * (1 - xi) * (1 - et)
    dZt[1] = -0.125 * (1 + xi) * (1 - et)
    dZt[2] = -0.125 * (1 + xi) * (1 + et)
    dZt[3] = -0.125 * (1 - xi) * (1 + et)
    dZt[4] = 0.125 * (1 - xi) * (1 - et)
    dZt[5] = 0.125 * (1 + xi) * (1 - et)
    dZt[6] = 0.125 * (1 + xi) * (1 + et)
    dZt[7] = 0.125 * (1 - xi) * (1 + et)

def H20ShapeFunction(xi, et, zt, h, dXi, dEt, dZt):
    h[0] = 0.125 * (1 - xi) * (1 - et) * (1 - zt) * (-2 - xi - et - zt)
    h[1] = 0.125 * (1 + xi) * (1 - et) * (1 - zt) * (-2 + xi - et - zt)
    h[2] = 0.125 * (1 + xi) * (1 + et) * (1 - zt) * (-2 + xi + et - zt)
    h[3] = 0.125 * (1 - xi) * (1 + et) * (1 - zt) * (-2 - xi + et - zt)

    h[4] = 0.125 * (1 - xi) * (1 - et) * (1 + zt) * (-2 - xi - et + zt)
    h[5] = 0.125 * (1 + xi) * (1 - et) * (1 + zt) * (-2 + xi - et + zt)
    h[6] = 0.125 * (1 + xi) * (1 + et) * (1 + zt) * (-2 + xi + et + zt)
    h[7] = 0.125 * (1 - xi) * (1 + et) * (1 + zt) * (-2 - xi + et + zt)

    h[8] = 0.25 * (1 - xi * xi) * (1 - et) * (1 - zt)
    h[10] = 0.25 * (1 - xi * xi) * (1 + et) * (1 - zt)
    h[14] = 0.25 * (1 - xi * xi) * (1 + et) * (1 + zt)
    h[12] = 0.25 * (1 - xi * xi) * (1 - et) * (1 + zt)

    h[9] = 0.25 * (1 - et * et) * (1 + xi) * (1 - zt)
    h[13] = 0.25 * (1 - et * et) * (1 + xi) * (1 + zt)
    h[15] = 0.25 * (1 - et * et) * (1 - xi) * (1 + zt)
    h[11] = 0.25 * (1 - et * et) * (1 - xi) * (1 - zt)

    h[16] = 0.25 * (1 - zt * zt) * (1 - xi) * (1 - et)
    h[17] = 0.25 * (1 - zt * zt) * (1 + xi) * (1 - et)
    h[18] = 0.25 * (1 - zt * zt) * (1 + xi) * (1 + et)
    h[19] = 0.25 * (1 - zt * zt) * (1 - xi) * (1 + et)

    dXi[0] = -0.125 * (1 - et) * (1 - zt) * (-1 - 2 * xi - et - zt)
    dXi[1] = 0.125 * (1 - et) * (1 - zt) * (-1 + 2 * xi - et - zt)
    dXi[2] = 0.125 * (1 + et) * (1 - zt) * (-1 + 2 * xi + et - zt)
    dXi[3] = -0.125 * (1 + et) * (1 - zt) * (-1 - 2 * xi + et - zt)

    dXi[4] = -0.125 * (1 - et) * (1 + zt) * (-1 - 2 * xi - et + zt)
    dXi[5] = 0.125 * (1 - et) * (1 + zt) * (-1 + 2 * xi - et + zt)
    dXi[6] = 0.125 * (1 + et) * (1 + zt) * (-1 + 2 * xi + et + zt)
    dXi[7] = -0.125 * (1 + et) * (1 + zt) * (-1 - 2 * xi + et + zt)

    dXi[8] = -0.5 * xi * (1 - et) * (1 - zt)
    dXi[10] = -0.5 * xi * (1 + et) * (1 - zt)
    dXi[14] = -0.5 * xi * (1 + et) * (1 + zt)
    dXi[12] = -0.5 * xi * (1 - et) * (1 + zt)

    dXi[9] = 0.25 * (1 - et * et) * (1 - zt)
    dXi[13] = 0.25 * (1 - et * et) * (1 + zt)
    dXi[15] = -0.25 * (1 - et * et) * (1 + zt)
    dXi[11] = -0.25 * (1 - et * et) * (1 - zt)

    dXi[16] = -0.25 * (1 - zt * zt) * (1 - et)
    dXi[17] = 0.25 * (1 - zt * zt) * (1 - et)
    dXi[18] = 0.25 * (1 - zt * zt) * (1 + et)
    dXi[19] = -0.25 * (1 - zt * zt) * (1 + et)

    dEt[0] = -0.125 * (1 - xi) * (1 - zt) * (-1 - xi - 2 * et - zt)
    dEt[1] = -0.125 * (1 + xi) * (1 - zt) * (-1 + xi - 2 * et - zt)
    dEt[2] = 0.125 * (1 + xi) * (1 - zt) * (-1 + xi + 2 * et - zt)
    dEt[3] = 0.125 * (1 - xi) * (1 - zt) * (-1 - xi + 2 * et - zt)

    dEt[4] = -0.125 * (1 - xi) * (1 + zt) * (-1 - xi - 2 * et + zt)
    dEt[5] = -0.125 * (1 + xi) * (1 + zt) * (-1 + xi - 2 * et + zt)
    dEt[6] = 0.125 * (1 + xi) * (1 + zt) * (-1 + xi + 2 * et + zt)
    dEt[7] = 0.125 * (1 - xi) * (1 + zt) * (-1 - xi + 2 * et + zt)

    dEt[8] = -0.25 * (1 - xi * xi) * (1 - zt)
    dEt[10] = 0.25 * (1 - xi * xi) * (1 - zt)
    dEt[14] = 0.25 * (1 - xi * xi) * (1 + zt)
    dEt[12] = -0.25 * (1 - xi * xi) * (1 + zt)

    dEt[9] = -0.5 * et * (1 + xi) * (1 - zt)
    dEt[13] = -0.5 * et * (1 + xi) * (1 + zt)
    dEt[15] = -0.5 * et * (1 - xi) * (1 + zt)
    dEt[11] = -0.5 * et * (1 - xi) * (1 - zt)

    dEt[16] = -0.25 * (1 - zt * zt) * (1 - xi)
    dEt[17] = -0.25 * (1 - zt * zt) * (1 + xi)
    dEt[18] = 0.25 * (1 - zt * zt) * (1 + xi)
    dEt[19] = 0.25 * (1 - zt * zt) * (1 - xi)

    dZt[0] = -0.125 * (1 - xi) * (1 - et) * (-1 - xi - et - 2 * zt)
    dZt[1] = -0.125 * (1 + xi) * (1 - et) * (-1 + xi - et - 2 * zt)
    dZt[2] = -0.125 * (1 + xi) * (1 + et) * (-1 + xi + et - 2 * zt)
    dZt[3] = -0.125 * (1 - xi) * (1 + et) * (-1 - xi + et - 2 * zt)

    dZt[4] = 0.125 * (1 - xi) * (1 - et) * (-1 - xi - et + 2 * zt)
    dZt[5] = 0.125 * (1 + xi) * (1 - et) * (-1 + xi - et + 2 * zt)
    dZt[6] = 0.125 * (1 + xi) * (1 + et) * (-1 + xi + et + 2 * zt)
    dZt[7] = 0.125 * (1 - xi) * (1 + et) * (-1 - xi + et + 2 * zt)

    dZt[8] = -0.25 * (1 - xi * xi) * (1 - et)
    dZt[10] = -0.25 * (1 - xi * xi) * (1 + et)
    dZt[14] = 0.25 * (1 - xi * xi) * (1 + et)
    dZt[12] = 0.25 * (1 - xi * xi) * (1 - et)

    dZt[9] = -0.25 * (1 - et * et) * (1 + xi)
    dZt[13] = 0.25 * (1 - et * et) * (1 + xi)
    dZt[15] = 0.25 * (1 - et * et) * (1 - xi)
    dZt[11] = -0.25 * (1 - et * et) * (1 - xi)

    dZt[16] = -0.5 * zt * (1 - xi) * (1 - et)
    dZt[17] = -0.5 * zt * (1 + xi) * (1 - et)
    dZt[18] = -0.5 * zt * (1 + xi) * (1 + et)
    dZt[19] = -0.5 * zt * (1 - xi) * (1 + et)

def T6ShapeFunction(xy, L):
    xxyy = xy[0:2, 0:1]
    grad, area= gradient2DT3(xxyy)
    dxL, dyL = grad[:][0], grad[:][1]
    L1, L2, L3 = L[0], L[1], L[2]
    N = np.zeros(5)
    N[0] = L1 * (2 * L1 - 1)
    N[1] = L2 * (2 * L2 - 1)
    N[2] = L3 * (2 * L3 - 1)
    N[3] = 4 * L2 * L3
    N[4] = 4 * L3 * L1
    N[5] = 4 * L1 * L2
    gradN = np.zeros(5, 2)
    gradN[0][0] = 4 * dxL[0] * L1 - dxL[0]
    gradN[1][0] = 4 * dxL[1] * L2 - dxL[1]
    gradN[2][0] = 4 * dxL[2] * L3 - dxL[2]
    gradN[3][0] = 4 * (dxL[0] * L2 + L1 * dxL[1])
    gradN[4][0] = 4 * (dxL[1] * L3 + L2 * dxL[2])
    gradN[5][0] = 4 * (dxL[0] * L3 + L1 * dxL[2])
    gradN[0][1] = 4 * dyL[0] * L1 - dyL[0]
    gradN[1][1] = 4 * dyL[1] * L2 - dyL[1]
    gradN[2][1] = 4 * dyL[2] * L3 - dyL[2]
    gradN[3][1] = 4 * (dyL[0] * L2 + L1 * dyL[1])
    gradN[4][1] = 4 * (dyL[1] * L3 + L2 * dyL[2])
    gradN[5][1] = 4 * (dyL[0] * L3 + L1 * dyL[2])
    return N, gradN, area

def ISOMap2D(isoFunc, x, y, xi, et, v, dx, dy):
    n = len(x)
    v = np.zeros(n)
    dx = np.zeros(n)
    dy = np.zeros(n)
    dXi = np.zeros(n)
    dEt = np.zeros(n)
    isoFunc(xi, et, v, dXi, dEt)
    j11 = np.dot(dXi, x)
    j12 = np.dot(dXi, y)
    j21 = np.dot(dEt, x)
    j22 = np.dot(dEt, y)
    detJ = j11 * j22 - j12 * j21
    for i in range(n):
        dx[i] = (j22 * dXi[i] - j12 * dEt[i]) / detJ
        dy[i] = (-j21 * dXi[i] + j11 * dEt[i]) / detJ
    return v, dx, dy, detJ;

def ISOMap3D(isoFunc, x, y, z, xi, et, zt, v, dx, dy, dz):
    n = len(x)
    v = np.zeros(n)
    dXi = np.zeros(n)
    dEt = np.zeros(n)
    dZt = np.zeros(n)
    isoFunc(xi, et, zt, v, dXi, dEt, dZt)
    j11 = np.dot(dXi, x)
    j12 = np.dot(dXi, y)
    j13 = np.dot(dXi, z)
    j21 = np.dot(dEt, x)
    j22 = np.dot(dEt, y)
    j23 = np.dot(dEt, z)
    j31 = np.dot(dZt, x)
    j32 = np.dot(dZt, y)
    j33 = np.dot(dZt, z)
    detJ = j11 * (j22 * j33 - j32 * j23) - j12 * (j21 * j33 - j31 * j23) + j13 * (j21 * j32 - j31 * j22)
    B11 = j22 * j33 - j32 * j23
    B21 = -(j21 * j33 - j31 * j23)
    B31 = j21 * j32 - j31 * j22
    B12 = -(j12 * j33 - j32 * j13)
    B22 = j11 * j33 - j31 * j13
    B32 = -(j11 * j32 - j31 * j12)
    B13 = j12 * j23 - j22 * j13
    B23 = -(j11 * j23 - j21 * j13)
    B33 = j11 * j22 - j21 * j12
    dx = (dXi * B11 + dEt * B12 + dZt * B13) / detJ
    dy = (dXi * B21 + dEt * B22 + dZt * B23) / detJ
    dz = (dXi * B31 + dEt * B32 + dZt * B33) / detJ
    return v, dx, dy, dz, detJ

def ISOMap3DTo2D(isoFunc, x, y, z, xi, et, u):
    n = len(x)
    dXi = np.zeros(n)
    dEt = np.zeros(n)
    isoFunc(xi, et, u, dXi, dEt)
    j11 = np.dot(dXi, x)
    j12 = np.dot(dXi, y)
    j13 = np.dot(dXi, z)
    j21 = np.dot(dEt, x)
    j22 = np.dot(dEt, y)
    j23 = np.dot(dEt, z)
    gx = j12 * j23 - j22 * j13
    gy = j21 * j13 - j11 * j23
    gz = j11 * j22 - j21 * j12
    detJ = np.sqrt(gx * gx + gy * gy + gz * gz)
    return detJ