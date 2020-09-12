from mesh.AbstractMesh import AMesh


class Mesh1DL2(AMesh):
    def __init__(self):
        AMesh.__init__(self)
        self.nDim = 1
        self.nPerElement = 2
        self.nPerBoundary = 1
        self.nEdgePerElement = 1
        self.nEdgePerBoundary = 0
        self.tecplotType = "FELINESEG"
        self.nBoundaryPerElement = 2
