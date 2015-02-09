from main import *


class Human(object):
    pass


class Man(Human):
    pass


class Woman(Human):
    pass


def God():
    adam, eve = Man(), Woman()
    return [adam, eve]


paradise = God()
test.assert_equals(True, isinstance(paradise[0], Man), "First object are a man")