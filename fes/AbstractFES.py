class FES:
    def __init__(self, mesh, dofPerNode):
        self.mesh = mesh
        self.dofPerNode = dofPerNode
        self.nDof = dofPerNode * mesh.NumberOfNodes
        self.dofPerElement = dofPerNode * self.nPerElement
        self.dofPerBoundary = dofPerNode * self.nPerBoundary
