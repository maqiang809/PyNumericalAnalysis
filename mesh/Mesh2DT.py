from matplotlib import cm
import numpy as np
import abc
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
    def scale(self, sx, sy):
        for i in range(self.nv):
            x = self.nodes[i, 0]
            y = self.nodes[i, 1]
            self.nodes[i, 0] = sx * x
            self.nodes[i, 1] = sy * y
    def transform(self, fx, fy):
        for i in range(self.nv):
            x, y = self.nodes[i, 0], self.nodes[i, 1]
            self.nodes[i, 0] = fx(x, y)
            self.nodes[i, 1] = fy(x, y)
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

