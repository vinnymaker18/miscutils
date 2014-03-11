# Contains 2d geometry routines useful for programming contests. Basic Vector arith-
# metic, polygon area, convex hull routines are implemented.

from math import asin, pi, sqrt

# A very small value, used for comparisions with zero.
EPS = 1e-9

# All the routines accept and return (x, y) tuples for vectors and 2d points.
# v* represent vectors while p* and q* represent points. a,b,c etc.. represent
# scalar values(reals) and x,y,z represent the individual coordinates themselves.

def cross_product(v1, v2):
    """Cross product of two 2d vectors is a vector
       perpendicular to both these vectors. Return value is a
       scalar representing the magniture and direction(towards
       positive/negative z-axis) of the cross product.
    """

    (x1, y1), (x2, y2) = v1, v2
    return x1*y2 - x2*y1


def dot_product(v1, v2):
    """Dot product of two vectors is a scalar that, when norm, measures
    how colinear are the two input vectors. e.g. v1.v2/|v1||v2| = -1 implies$
    they are alignedexactly opposite to each other, while a value of 1 implies 
    that they are aligned in the same direction.
    """

    (x1, y1), (x2, y2) = v1, v2
    return x1*x2 + y1*y2

def vector_magnitude(v):
    """ Returns the magnitude of the given vector"""

    (x1, y1) = v
    return sqrt(x1*x1 + y1*y1)


def vector_add(v1, v2):
    """ Returns the vector addition of the two vectors"""

    (x1, y1), (x2, y2) = v1, v2
    return (x1+x2, y1+y2)

def scalar_mult(v, a):
    """ Scalar multiplication of vector v with the scalar a"""
    (x, y) = v
    return (a*x, a*y)

# turn angle is useful is polygon routines like graham's scan etc..
def turn_angle(v1, v2):
    """How much angleto turn anti-clockwise as we change our direction from v1 to
    v2. Units are radians"""
    m1,m2 = map(vector_magnitude, [v1, v2])
    
    # Special case is when one of the vectors is a zero vector.
    if m1 <= EPS or m2 <= EPS:
        return 0

    # v1 cross v2 = |v1| |v2| sin(theta) where theta is the angle b/w them.
    norm_crossp = cross_product(v1, v2) / m1 / m2
    norm_dotp = dot_product(v1, v2) / m1 / m2

    if norm_crossp >= -EPS:
        # turned not more than 180 degrees anti-clockwise.
        if norm_dotp >= -EPS:
            # not more than 90.
            return asin(norm_crossp)

        return pi - asin(norm_crossp)

    # turned more than 180 degrees anti-clockwise.
    if norm_dotp > -EPS:
        return 2*pi + asin(norm_crossp)

    return pi - asin(norm_crossp)


def point_dist(p, q):
    """ Euclidean distance b/w p and q"""
    (x1, y1), (x2, y2) = p, q
    dx, dy = (x2-x1, y2-y1)
    return sqrt(dx*dx + dy*dy)


# Equation of the line passing through p and q. Return value is of form
# (a,b,c) where ax+by+c = 0 is the equation.
def line_equation(p, q):
    """ Equation of the line passing through p and q"""

    if point_dist(p, q) <= EPS:
        # p and q are the same point.
        raise ValueError("Two points are the same")

    (x1, y1), (x2, y2) = p, q
    if abs(x1-x2) <= EPS:
        # the vertical line x = x1
        return (1.0, 0.0, -x1 + 0.0)
    
    m = (y2-y1) / (x2-x1 + 0.0)
    c = y1-m*x1

    return (m, -1, c)


def point_on_segment(p, q1, q2):
    """Returns true if p lies on the line segment joining q1 and q2"""
    pq1 = point_dist(p, q1)
    pq2 = point_dist(p, q2)
    q1q2 = point_dist(q1, q2)

    # From the triangle inequality, |AB| + |BC| > |AC| unless B is colinear
    # w.r.t A <-> C. And |AB| + |BC| = |AC| when B lies in b/w A and C.
    return abs((pq1 + pq2) - q1q2) <= EPS
    

# Intersection of lines p1<->q1 and p2<->q2. Line p <-> q denotes a line
# joining the points p and q.
def lines_intersect(p1, q1, p2, q2, segments = False):
    """Checks whether the given lines intersect. 
    segments : boolean value for line segments intersection.
    """

    (a1, b1, c1) = line_equation(p1, q1)
    (a2, b2, c2) = line_equation(p2, q2)

    if abs(a1*b2-a2*b1) <= EPS:
        # Parallel lines or colinear lines. Return None.
        return None

    x = (c2*b1-c1*b2) / (a1*b2 - a2*b1)
    y = (c2*a1-c1*a2) / (b1*a2 - b2*a1)

    if segments:
        # check whether the point lies on both the segments
        return (x, y) if point_on_segment((x,y), p1, q1)\
            and point_on_segment((x, y), p2, q2) else None

    return (x, y)
    
####################################################################################

def main():
    print "2d geometry module"

if __name__ == '__main__':
    main()
