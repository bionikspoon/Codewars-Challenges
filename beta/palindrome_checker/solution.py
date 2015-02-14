from main import test
from re import findall


def is_palindrome(s):
    s = "".join(findall(r'[a-z]*', s.lower()))
    return True if s[::-1] == s else False


test.assert_equals(is_palindrome(""), True)
test.assert_equals(is_palindrome("maoam"), True)
test.assert_equals(is_palindrome("abc"), False)
test.assert_equals(is_palindrome("If I had a hi-fi..."), True)