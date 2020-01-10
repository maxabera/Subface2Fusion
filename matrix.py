__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

from fractions import Fraction
from . import units
from . import app_context
import math


def is_zero(a):
    return equals(a, identity(4))


def equals( a, b):
    assert(len(a) == len(b))
    assert(len(a[0]) == len(b[0]))
    for i in range(len(a)):
        for j in range(len(a[0])):
            if not math.isclose(a[i][j], b[i][j]):
                return False
    return True


# multiply
def mtx_mlt(A,B):
    return [[sum([A[i][m]*B[m][j] for m in range(len(A[0]))]) for j in range(len(B[0]))] for i in range(len(A))]


# Return Identity Matrix One Liner
def identity(n):
    return [[1 if i == j else 0 for i in range(n)] for j in range(n)]


ident_matrix = identity(4)


def inverse(mat):
    i_mat = identity(len(mat))
    MI = [mat[i] + i_mat[i] for i in range(len(mat))]
    for i in range(len(MI)):
        if MI[i][i] == 0:
            temp = mat[i]
            mat[i] = mat[i + 1]
            mat[i + 1] = temp
        if MI[i][i] != 1:
            h = MI[i][i]
            for j in range(len(MI[0])):
                MI[i][j] = Fraction(MI[i][j],h)
        for r in range(len(MI)):
            if r != i:
                h = MI[r][i]
                for c in range(len(MI[0])):
                    MI[r][c] -= h*MI[i][c]
        return [i[-len(mat):] for i in MI]


def serialize(m):
    # convert
    tm = list()
    for row in m:
        for cell in row:
            tm.append(cell)
    return tm


