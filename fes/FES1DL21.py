from fes.AbstractFES import FES
from fes.ElementMatrices import elementStiff1DL2
from fes.ElementVectors import elementSource1DL2


class FES1DL21(FES):
    def __init__(self, mesh):
        FES.__init__(self, mesh, 1)

    def assembleStiff_const(self, coef, tp, A):
        self.assembleGlobalMatrix_Const(coef, elementStiff1DL2, tp, A)

    def assembleSource_const(self, coef, tp, VEC):
        self.assembleGlobalVector_Const(coef, elementSource1DL2, tp, VEC)




