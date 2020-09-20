from fes.AbstractFES import FES
from fes.ElementMatrices import elementHeatStiff2DT3
from fes.ElementVectors import elementSource2DT3


class FES2DT31(FES):
    def __init__(self, mesh):
        FES.__init__(self, mesh, 1)

    def assembleStiff(self, coef, param, tp, A):
        self.assembleGlobalMatrix(coef, param, elementHeatStiff2DT3, tp, A)
    def assembleStiff_const(self, coef, tp, A):
        self.assembleGlobalMatrix_Const(coef, elementHeatStiff2DT3, tp, A)

    def assembleSource_const(self, coef, tp, VEC):
        self.assembleGlobalVector_Const(coef, elementSource2DT3, tp, VEC)

    def assembleSource_func(self, coef, param, tp, VEC):
        self.assembleGlobalVector_Func(coef, param, elementSource2DT3, tp, VEC)