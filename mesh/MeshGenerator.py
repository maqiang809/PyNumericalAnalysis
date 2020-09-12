from mesh.Mesh1DL import Mesh1DL2

def line1DL2(a, b, num):
    mesh = Mesh1DL2()
    nv = num + 1
    nt = num
    nb = 2
    mesh.initMesh0(nv, nt, nb)
    for i in range(nv):
        mesh.nodes[i, 0] = a + (b - a) / num * i
    for i in range(nt):
        mesh.elements[i, 0] = i
        mesh.elements[i, 1] = i + 1
    mesh.boundaries[0, 0] = 0
    mesh.boundaryLabel[0] = 1
    mesh.boundaries[1, 0] = num
    mesh.boundaryLabel[1] = 2
    return mesh

mesh = line1DL2(0.0, 1.0, 10)
mesh.printNodes()
mesh.printElements()
mesh.printBoundaries()
mesh.saveMesh("mymesh1D.txt")