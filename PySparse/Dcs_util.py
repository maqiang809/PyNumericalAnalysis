from PySparse.Dcs_common import Dcs, Dcsd
import numpy as np

class Dcs_util:
    # /**
    #  * Allocate a sparse matrix (triplet form or compressed-column form).
    #  *
    #  * @param m
    #  *            number of rows
    #  * @param n
    #  *            number of columns
    #  * @param nzmax
    #  *            maximum number of entries
    #  * @param values
    #  *            allocate pattern only if false, values and pattern otherwise
    #  * @param triplet
    #  *            compressed-column if false, triplet form otherwise
    #  * @return sparse matrix
    #  */
    @classmethod
    def cs_spalloc(self, m, n, nzmax, values, triplet):
        A = Dcs
        A.m = m
        A.n = n
        A.nzmax = nzmax = np.max(nzmax, 1);
        A.nz = 0 if triplet else -1
        A.p = np.zeros(nzmax) if triplet else np.zeros(n + 1)
        A.i = np.zeros(nzmax)
        A.x = np.zeros(nzmax) if values else None
        return A

    # /**
    #  * Change the max # of entries a sparse matrix can hold.
    #  *
    #  * @param A
    #  *            column-compressed matrix
    #  * @param nzmax
    #  *            new maximum number of entries
    #  * @return true if successful, false on error
    #  */
    @classmethod
    def cs_sprealloc(self, A, nzmax):
        if A is None:
            return False
        if nzmax <= 0:
            nzmax = A.p[A.n] if Dcs_util.CS_CSC(A) else A.nz
        Ainew = np.zeros(nzmax)
        length = np.min(nzmax, len(A.i))
        for i in range(length):
            Ainew[i] = A.i[i]
        A.i = Ainew
        if Dcs_util.CS_TRIPLET(A):
            Apnew = np.zeros(nzmax)
            length = np.min(nzmax, len(A.p));
            for i in range(length):
                Apnew[i] = A.p[i]
            A.p = Apnew
        if A.x is not None:
            Axnew = np.zeros(nzmax)
            length = np.min(nzmax, len(A.x))
            for i in range(length):
                Axnew[i] = A.x[i]
            A.x = Axnew
        A.nzmax = nzmax
        return True

    # /**
    #  * Allocate a Dcsd object (a Dulmage-Mendelsohn decomposition).
    #  *
    #  * @param m
    #  *            number of rows of the matrix A to be analyzed
    #  * @param n
    #  *            number of columns of the matrix A to be analyzed
    #  * @return Dulmage-Mendelsohn decomposition
    #  */
    @classmethod
    def cs_dalloc(self, m, n):
        D = Dcsd
        D.p = np.zeros(m)
        D.r = np.zeros(m + 6)
        D.q = np.zeros(n)
        D.s = np.zeros(n + 6)
        D.cc = np.zeros(5)
        D.rr = np.zeros(5)
        return D

    @classmethod
    def CS_FLIP(self, i):
        return (-(i) - 2)

    @classmethod
    def CS_UNFLIP(self, i):
        return self.CS_FLIP(i) if i < 0 else i

    @classmethod
    def CS_MARKED(self, w, j):
        return w[j] < 0

    @classmethod
    def CS_MARK(self, w, j):
        w[j] = self.CS_FLIP(w[j])

    # /**
    #  * Returns true if A is in column-compressed form, false otherwise.
    #  *
    #  * @param A
    #  *            sparse matrix
    #  * @return true if A is in column-compressed form, false otherwise
    #  */
    @classmethod
    def CS_CSC(self, A):
        return A is not None and A.nz == -1

    # /**
    #  * Returns true if A is in triplet form, false otherwise.
    #  *
    #  * @param A
    #  *            sparse matrix
    #  * @return true if A is in triplet form, false otherwise
    #  */
    @classmethod
    def CS_TRIPLET(self, A):
        return A is not None and A.nz >= 0
