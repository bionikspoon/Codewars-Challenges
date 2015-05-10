from main import *

add = sum

def sum(*args):
    return add(arg for arg in args if isinstance(arg, int))


test.assert_equals(sum(1, 2, 3), 6)
test.assert_equals(sum(1, 2, 3, "bear"), 6)