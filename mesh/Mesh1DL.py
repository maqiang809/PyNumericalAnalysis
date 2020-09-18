from mesh.AbstractMesh import AMesh
import matplotlib.pyplot as plt
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

    def plotSolution(self, x, xLabel, yLabel, title):
        plt.plot(self.nodes, x)
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)
        plt.title(title)
        plt.show()
