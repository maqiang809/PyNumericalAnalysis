from matplotlib import cm

from mesh.AbstractMesh import AMesh
import matplotlib.pyplot as plt
from matplotlib import *

class Mesh2DT3(AMesh):
    def __init__(self):
        AMesh.__init__(self)
        self.nDim = 2
        self.nPerElement = 3
        self.nPerBoundary = 2
        self.nEdgePerElement = 3
        self.nBoundaryPerElement = 3
        self.nEdgePerBoundary = 1
        self.tecplotType = "FETRIANGLE"

    def plotMesh(self):
        plt.figure()
        plt.gca().set_aspect('equal')
        plt.triplot(self.nodes[:, 0], self.nodes[:, 1], self.elements, lw=0.5, color='k')
        plt.show()

    def plotSolution(self, u):
        plt.figure()
        plt.gca().set_aspect('equal')
        mapper = plt.tripcolor(self.nodes[:, 0], self.nodes[:, 1], self.elements, u, shading='gouraud', cmap=cm.jet)
        #plt.tricontour(x, y, triangles, u, 0)
        #plt.tricontourf(x, y, triangles, u)
        plt.colorbar(mapper, label="temperature")
        plt.triplot(self.nodes[:, 0], self.nodes[:, 1], self.elements, lw=0.5, alpha=0.3, color="k")
        plt.show()