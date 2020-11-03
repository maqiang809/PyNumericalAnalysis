from mesh.MeshGenerator import square2D
import numpy as np
mymesh = square2D(100, 10, 1)
mymesh.plotMesh()
mymesh.scale(10.0, 1.0)
mymesh.plotMesh()

mymesh2 = square2D(10, 30, 1);
fx = lambda x, y:(x + 1) * np.cos(np.pi * y)
fy = lambda x, y:(x + 1) * np.sin(np.pi * y)
mymesh2.transform(fx, fy)
mymesh2.plotMesh()

mymesh3 = square2D(20, 20, 1)
fx1 = lambda x, y: x
fy1 = lambda x, y : (x + 1) * y
mymesh3.transform(fx1, fy1)
mymesh3.plotMesh()