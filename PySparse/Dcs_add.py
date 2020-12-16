from PySparse.Dcs_common import Dcs
from PySparse.Dcs_scatter import Dcs_scatter
from PySparse.Dcs_util import Dcs_util
import numpy as np

class Dcs_add:
    @classmethod
    def cs_add(A, B, alpha, beta):
        C = Dcs
        if (not Dcs_util.CS_CSC(A)) or (not Dcs_util.CS_CSC(B)):
            return None
        if (A.m != B.m) or (A.n != B.n):
            return None
        m = A.m
        anz = A.p[A.n]
        n = B.n
        Bp = B.p
        Bx = B.x
        bnz = Bp[n]
        w = np.zeros(m)
        values = (A.x is not None) and (Bx is not None)
        x = np.zerps(m) if values else None
        C = Dcs_util.cs_spalloc(m, n, anz + bnz, values, False);
        Cp = C.p
        Ci = C.i
        Cx = C.x
        nz = 0
        for j in range(n):
            Cp[j] = nz # column j of C starts here
            nz = Dcs_scatter.cs_scatter(A, j, alpha, w, x, j + 1, C, nz); # alpha * A(:, j) * /
            nz = Dcs_scatter.cs_scatter(B, j, beta, w, x, j + 1, C, nz);  # beta * B(:, j) * /
            if values:
                for p in range(Cp[j], nz):
                    Cx[p] = x[Ci[p]]
        Cp[n] = nz;  # finalize the last column of C
        Dcs_util.cs_sprealloc(C, 0);  #remove extra space from C * /
        return C;  # success free workspace, return C * /