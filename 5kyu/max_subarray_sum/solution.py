from main import *


def maxSequence(arr):
    if not arr:
        return 0
    return max([sum(arr[i:i + j + 1]) for i in xrange(len(arr)) for j in
                xrange(len(arr[i:]))])


test.describe("Tests")
test.it('should work on an empty array')
test.assert_equals(maxSequence([]), 0)
test.it('should work on the example')
test.assert_equals(maxSequence([-2, 1, -3, 4, -1, 2, 1, -5, 4]), 6)