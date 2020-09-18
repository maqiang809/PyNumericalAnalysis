from fes.ComputationalGeometry import *

def elementStiff1DL2(coord, coef, tp, eleMatrix):
    grad, len = gradient1DL2(coord)
    if tp == "COMMON":
        coef = 0.5 * np.sum(coef[0]) / len;
        eleMatrix[0][0] = eleMatrix[1][1] = coef;
        eleMatrix[0][1] = eleMatrix[1][0] = -coef;
    else:
        raise ValueError("Wrong BVPType!")

def elementHeatStiff2DT3(coord, coef, tp, eleMatrix):
    grad, area = gradient2DT3(coord)
    # eleMatrix = np.zeros((3, 3), dtype=np.float64)
    if tp == "COMMON":
        Af = area * np.average(coef[0])
        for i in range(3):
            eleMatrix[i, :] = Af * (grad[i, 0] * grad[:, 0] + grad[i, 1] * grad[:, 1])
    elif tp == "AXISYMMETRIC":
        x = coord[:, 0]
        Af = area * (np.sum(coef[0]) * np.sum(x) + np.dot(coef[0], x)) / 12.0
        for i in range(3):
            eleMatrix[i, :] = Af * (grad[i, 0] * grad[:, 0] + grad[i, 1] * grad[:, 1])
    elif tp == "MATRIX_COMMON":
        eleMatrix[:, :] = np.dot(np.dot(grad, coef), np.transpose(grad)) * area
    elif tp == "MATRIX_AXIS":
        eleMatrix[:, :] = np.dot(np.dot(grad, coef), np.transpose(grad)) * (area * np.average(coord[:, 0]))
    else:
        raise ValueError("Wrong BVPType!")