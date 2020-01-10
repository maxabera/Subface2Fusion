__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

import math

def norm(vector):
    a = vector[0]
    b = vector[1]
    c = vector[2]
    return math.sqrt( a*a + b*b + c*c )
    
def create(p0, p1):
    a = p1[0]-p0[0]
    b = p1[1]-p0[1]
    c = p1[2]-p0[2]
    return [a, b, c]
    
def dot(vec0, vec1):    
    return (vec0[0]*vec1[0]) + (vec0[1]*vec1[1]) + (vec0[2]*vec1[2])
    
def cross(vec0, vec1):
    nv = [0, 0, 0]
    nv[0] = (vec0[1]*vec1[2]) - (vec0[2]*vec1[1])
    nv[1] = (vec0[2]*vec1[0]) - (vec0[0]*vec1[2])
    nv[2] = (vec0[0]*vec1[1]) - (vec0[1]*vec1[0])
    return nv
    
def magnitude(vec0):
    sq = dot(vec0, vec0)
    return math.sqrt(sq)

def distance(p0, p1):
    vec = create(p0, p1)
    return magnitude(vec)

def is_zero(vec, eps=0.00000001):
    return math.isclose(norm(vec), 0, rel_tol=eps)

def is_equal(vec0, vec1, eps=0.00000001):
    for i in range(3):
        if not math.isclose(vec0[i], vec1[i], abs_tol=eps):
            return False
    return True
