"""Contains 2d geometry routines useful for programming contests.
Basic Vector arith-metic, polygon area, convex hull routines are implemented.
"""

from math import asin, pi, sqrt

# A very small value, used for comparisions with zero.
EPS = 1e-9

# Points and vectors are considered different in this module.
# All the routines accept and return (x, y) tuples for vectors and 2d points.


def cross_product(vec1, vec2):
    """Cross product of two 2d vectors is a vector
       perpendicular to both these vectors. Return value is a
       scalar representing the magnitude and direction(towards
       positive/negative z-axis) of the cross product.
    """

    (px1, py1), (px2, py2) = vec1, vec2
    return px1 * py2 - px2 * py1


def dot_product(vec1, vec2):
    """Dot product of two vectors is a scalar that, when normalized, measures
    how colinear are the two input vectors. e.g. vec1.vec2/|vec1||vec2| = -1
    implies they are aligned exactly opposite to each other, while a value of 1
    implies that they are aligned in the same direction.
    """

    (px1, py1), (px2, py2) = vec1, vec2
    return px1 * px2 + py1 * py2


def vector_magnitude(vec):
    """ Returns the magnitude of the given vector"""

    (px1, py1) = vec
    return sqrt(px1 * px1 + py1 * py1)


def vector_add(vec1, vec2):
    """ Returns the vector addition of the two vectors"""

    (px1, py1), (px2, py2) = vec1, vec2
    return (px1 + px2, py1 + py2)


def scalar_mult(vec, fac):
    """ Scalar multiplication of vector v with the scalar a"""
    (ptx, pty) = vec
    return (fac * ptx, fac * pty)


# turn angle is useful is polygon routines like graham's scan etc..
def turn_angle(vec1, vec2):
    """How much angleto turn anti-clockwise as we change our direction from
    vec1 to vec2. Units are radians"""

    mag1, mag2 = [vector_magnitude(v) for v in [vec1, vec2]]

    # Special case is when one of the vectors is a zero vector.
    if mag1 <= EPS or mag2 <= EPS:
        return 0

    # vec1 cross vec2 = |vec1| |vec2| sin(theta) where theta is the angle
    # b/w them.
    norm_crossp = cross_product(vec1, vec2) / mag1 / mag2
    norm_dotp = dot_product(vec1, vec2) / mag1 / mag2

    if norm_crossp >= -EPS:
        # turned not more than 180 degrees anti-clockwise.
        if norm_dotp >= -EPS:
            # not more than 90.
            return asin(norm_crossp)

        return pi - asin(norm_crossp)

    # turned more than 180 degrees anti-clockwise.
    if norm_dotp > -EPS:
        return 2 * pi + asin(norm_crossp)

    return pi - asin(norm_crossp)


def point_dist(pt1, pt2):
    """ Euclidean distance b/w p and q"""

    (px1, py1), (px2, py2) = pt1, pt2
    d_x, d_y = (px2 - px1, py2 - py1)
    return sqrt(d_x * d_x + d_y * d_y)


# Equation of the line passing through p and q. Return value is of form
# (a,b,c) where ax+by+c = 0 is the equation.
def line_equation(pt1, pt2):
    """ Equation of the line passing through p and q"""

    if point_dist(pt1, pt2) <= EPS:
        # p and q are the same point.
        raise ValueError("Two points are the same")

    (px1, py1), (px2, py2) = pt1, pt2
    if abs(px1 - px2) <= EPS:
        # the vertical line x = px1
        return (1.0, 0.0, -px1 + 0.0)

    slope = (py2 - py1) / (px2 - px1 + 0.0)
    offset = py1 - slope * py1

    return (slope, -1, offset)


def point_on_segment(ptp, ptq1, ptq2):
    """Returns true if p lies on the line segment joining q1 and q2"""
    pq1 = point_dist(ptp, ptq1)
    pq2 = point_dist(ptp, ptq2)
    q1q2 = point_dist(ptq1, ptq2)

    # From the triangle inequality, |AB| + |BC| > |AC| unless B is colinear
    # w.r.t A <-> C. And |AB| + |BC| = |AC| when B lies in b/w A and C.
    return abs((pq1 + pq2) - q1q2) <= EPS


# Intersection of lines p1<->q1 and p2<->q2. Line p <-> q denotes a line
# joining the points p and q.
def lines_intersect(pt1, qt1, pt2, qt2, segments=False):
    """Checks whether the given lines intersect.
    segments : boolean value for line segments intersection.
    """

    (aa1, bb1, cc1) = line_equation(pt1, qt1)
    (aa2, bb2, cc2) = line_equation(pt2, qt2)

    if abs(aa1 * bb2 - aa2 * bb1) <= EPS:
        # Parallel lines or colinear lines. Return None.
        return None

    pxc = (cc2 * bb1 - cc1 * bb2) / (aa1 * bb2 - aa2 * bb1)
    pyc = (cc2 * aa1 - cc1 * aa2) / (bb1 * aa2 - bb2 * aa1)

    if segments:
        # check whether the point lies on both the segments
        return (pxc, pyc) if point_on_segment((pxc, pyc), pt1, qt1)\
            and point_on_segment((pxc, pyc), pt2, qt2) else None

    return (pxc, pyc)


# Convex hull of a set of points in 2d is the minimal convex polygon
# that encloses(or includes) all the points in the given set.
def convex_hull(pts):
    """Graham's scan algorithm. Complexity is O(nlogn) where n is
    the no. of points in pts. Returns the hull vertices in counter clockwise
    order.

    pts : A list of (x, y) tuples which are points. Assumes that
    the vertices are distinct.(Assumption not strictly necessary)
    """
    pts = list(pts)
    size = len(pts)
    if size < 3:
        return pts

    # Start with the vertex with the lowest y-coordinate. (Left most
    # one if several have the lowest y-coordinate) and call it V0.
    (px0, py0) = pts[0]
    for (ppx, ppy) in pts:
        if ppy < py0 or (ppy == py0 and ppx < px0):
            px0, py0 = ppx, ppy

    # Sort the vertices according to the angle they make with the V0X+
    pts[0], (px0, py0) = (px0, py0), pts[0]
    pts[1:] = sorted(pts[1:],
                     key=lambda (x, y): turn_angle((1, 0), (x - px0, y - py0
                                                            )
                                                   )
                     )

    # Scan through the sorted vertices in order and maintain the turn-left
    # property.
    def is_a_left_turn((px1, py1), (px2, py2), (px3, py3)):
        """Returns with p2->p3 is leftwards of p1->p2"""

        vec12, vec23 = (px2 - px1, py2 - py1), (px3 - px2, py3 - py2)
        angle_turned = turn_angle(vec12, vec23)
        return angle_turned <= pi - EPS

    stack = pts[0:2]
    for point in pts[2:]:
        while len(stack) >= 2 and \
                not is_a_left_turn(stack[-2], stack[-1], point):
            stack.pop()

        stack.append(point)

    return stack


# pts can be a list or a generator expression.
def poly_area(pts):
    """Area of the polygon with vertices `pts'. Assumes that the points are
    ordered clockwise or anti-clockwise. Users could compute the convex hull
    first and then compute the area, if their vertices are not ordered.
    """

    if len(pts) < 3:
        return 0

    area = 0
    for i in xrange(len(pts)):
        (px1, py1), (px2, py2) = pts[i], pts[(i + 1) % len(pts)]
        area += 0.5 * (px1 * py2 - px2 * py1)

    return abs(area)


def tri_area(p, q, r):
    """Triangle area"""

    (px1, py1), (px2, py2), (x3, y3) = p, q, r
    px2, py2, x3, y3 = px2 - px1, py2 - py1, x3 - px1, y3 - py1
    return 0.5 * abs(px2 * y3 - x3 * py2)


def main():
    """Do something when run as a script"""
    pass

if __name__ == '__main__':
    main()
