from PySparse.Dcs_util import Dcs_util


class Dcs_scatter:

    # /**
    #  * Scatters and sums a sparse vector A(:,j) into a dense vector, x = x +
    #  * beta * A(:,j).
    #  *
    #  * @param A
    #  *            the sparse vector is A(:,j)
    #  * @param j
    #  *            the column of A to use
    #  * @param beta
    #  *            scalar multiplied by A(:,j)
    #  * @param w
    #  *            size m, node i is marked if w[i] = mark
    #  * @param x
    #  *            size m, ignored if null
    #  * @param mark
    #  *            mark value of w
    #  * @param C
    #  *            pattern of x accumulated in C.i
    #  * @param nz
    #  *            pattern of x placed in C starting at C.i[nz]
    #  * @return new value of nz, -1 on error
    #  */
    @classmethod
    def cs_scatter(A, j, beta, w, x, mark, C, nz):
        if (not Dcs_util.CS_CSC(A)) or w is None or not Dcs_util.CS_CSC(C):
            return (-1) # check inputs
        Ap = A.p
        Ai = A.i
        Ax = A.x
        Ci = C.i
        for p in range(Ap[j], Ap[j+1]):
            i = Ai[p] #A(i,j) is nonzero */
            if (w[i] < mark):
                w[i] = mark # i is new entry in column j */
                Ci[nz] = i # add i to pattern of C(:,j) */
                nz += 1
                if x is not None:
                    x[i] = beta * Ax[p] # x(i) = beta*A(i,j) */
            elif x is not None:
                x[i] += beta * Ax[p] # i exists in C(:,j) already */
        return nz