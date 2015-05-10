from main import test

from fractions import Fraction
from math import factorial
from operator import mul


def number_of_arrangements(word):
    letter_counts = [factorial(word.count(i)) for i in set(word)]
    return factorial(len(word)) / reduce(mul, letter_counts)


def listPosition(word):
    """Return the anagram list position of the word"""
    position_score = [number_of_arrangements(word[k:]) for k, _ in
                      enumerate(word)]

    position_fraction = [Fraction(sorted(word[k:]).index(v), len(word[k:])) for
                         k, v in enumerate(word)]

    return sum([i * j for i, j in zip(position_score, position_fraction)]) + 1


test.assert_equals(number_of_arrangements("AAA"), 1)
test.assert_equals(number_of_arrangements("AAB"), 3)
test.assert_equals(number_of_arrangements("ABB"), 3)  # 3*1*1
test.assert_equals(number_of_arrangements("ABC"), 6)  # 3*2*1
test.assert_equals(number_of_arrangements("AAAB"), 4)  # 4
test.assert_equals(number_of_arrangements("AABC"), 12)  # 4*3*1*1
test.assert_equals(number_of_arrangements("ABCD"), 24)  # 4*3*2*1
test.assert_equals(number_of_arrangements("AABB"), 6)  #
test.assert_equals(number_of_arrangements("AAAAB"), 5)  # 5
test.assert_equals(number_of_arrangements("AAABC"), 20)  # 5*4

# 5*4*3*2*1/(3*2*1*2*1) == factorial(5)/factorial(2)
test.assert_equals(number_of_arrangements("AABCD"), 60)
test.assert_equals(number_of_arrangements("ABCDE"), 120)  # 5*4*3*2*1

# 5*4*3*2*1/(3*2*1*2*1) == factorial(5)/(factorial(3)*factorial(2))
test.assert_equals(number_of_arrangements("AAABB"), 10)

# 5*4*3*2*1/(2*1*2*1*1) == factorial(5)/(factorial(2)*factorial(2))
test.assert_equals(number_of_arrangements("AABBC"), 30)
test.assert_equals(number_of_arrangements("ABBBC"), 20)  # 5*2*3
test.assert_equals(number_of_arrangements("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
                   403291461126605635584000000)

test.describe('Anagram')
test.it('Must return appropriate values for known inputs')
testValues = {'A': 1, 'ABAB': 2, 'AAAB': 1, 'BAAA': 4, 'QUESTION': 24572,
              'BOOKKEEPER': 10743}
for word in testValues:
    test.assert_equals(listPosition(word), testValues[word],
                       'Incorrect list position for: ' + word)