from fes.ComputationalGeometry import length2DL2
import numpy as np

def elementSource1DL2(coord, coef, tp, eleVec):
    x = coord[:, 0]
    L = np.abs(x[1] - x[0])
    f = coef[0, :]
    if tp == "COMMON":
        eleVec[0] = (2 * f[0] + f[1]) * L / 6
        eleVec[1] = (f[0] + 2 * f[1]) * L / 6
    elif tp == "AXISYMMETRIC":
        eleVec[0] = (2 * x[0] * f[0] + np.sum(x) * np.sum(f)) * L / 12.0
        eleVec[1] = (2 * x[1] * f[1] + np.sum(x) * np.sum(f)) * L / 12.0
    elif tp == "SPHERICAL":
        eleVec[0] = (2 * x[0] * x[0] * f[0] + (x[0] * x[0] + x[1] * x[1]) * np.sum(f)) * L / 12.0
        eleVec[1] = (2 * x[1] * x[1] * f[1] + (x[0] * x[0] + x[1] * x[1]) * np.sum(f)) * L / 12.0
    else:
        raise ValueError("type wrong!")