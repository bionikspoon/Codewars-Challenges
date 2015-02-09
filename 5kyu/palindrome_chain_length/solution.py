from main import *


def palindrome_chain_length(n):
    count = 0
    while True:
        reversed_n = reverse_order(n)
        if is_palindrome(n, reversed_n):
            return count
        n += reversed_n
        count += 1


def reverse_order(n):
    return int("".join([i for i in list(str(n)[::-1])]))


def is_palindrome(n, reversed_n):
    return True if n == reversed_n else False


test.assert_equals(reverse_order(87), 78)
test.assert_equals(is_palindrome(87, reverse_order(87)), False)
test.assert_equals(is_palindrome(5, reverse_order(5)), True)
test.assert_equals(palindrome_chain_length(87), 4)