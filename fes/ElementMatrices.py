from fes.ComputationalGeometry import *


def elementHeatStiff2DT3(self, coord, coef, tp):
    grad, area = gradient2DT3(coord)
    eleMatrix = np.zeros((3, 3), dtype=np.float64)
    if tp == "COMMON":
        Af = area * np.average(coef[0])
        for i in range(3):
            eleMatrix[i, :] = Af * (grad[i, 0] * grad[:, 0] + grad[i, 1] * grad[:, 1])
        return eleMatrix
    elif tp == "AXISYMMETRIC":
        x = coord[:, 0]
        Af = area * (np.sum(coef[0]) * np.sum(x) + np.dot(coef[0], x)) / 12.0
        for i in range(3):
            eleMatrix[i, :] = Af * (grad[i, 0] * grad[:, 0] + grad[i, 1] * grad[:, 1])
        return eleMatrix
    elif tp == "MATRIX_COMMON":
        return np.dot(np.dot(grad, coef), np.transpose(grad)) * area
    elif tp == "MATRIX_AXIS":
        return np.dot(np.dot(grad, coef), np.transpose(grad)) * (area * np.average(coord[:, 0]))
    else:
        raise ValueError("Wrong BVPType!")