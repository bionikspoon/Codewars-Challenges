from main import test
from fractions import Fraction, gcd


def lcm(*args):
    """Compute the least common multiple of some non-negative integers"""
    if 0 in args:
        return 0
    return reduce(gcd, [Fraction(1, arg) for arg in args]) ** -1


test.assert_equals(lcm(2, 5), 10)
test.assert_equals(lcm(2, 3, 4), 12)
test.assert_equals(lcm(9), 9)
test.assert_equals(lcm(0), 0)
test.assert_equals(lcm(0, 1), 0)