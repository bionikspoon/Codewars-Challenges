#!/usr/bin/python
from TestHandler import TestHandler


Test = TestHandler()
test = Test

# noinspection PyUnresolvedReferences
import solution

test.dispatch_asserts()