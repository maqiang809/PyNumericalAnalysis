from fes.AbstractFES import FES


class FES1DL21(FES):
    def __init__(self, mesh):
        FES.__init__(mesh, 1)

