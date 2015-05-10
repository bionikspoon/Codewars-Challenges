from main import *


def square_digits(num):
    return int("".join(map(lambda x: str(int(x) ** 2), list(str(num)))))



test.assert_equals(square_digits(9119), 811181)