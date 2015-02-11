from main import *

from datetime import datetime


class Mongo(object):
    @classmethod
    def is_valid(cls, s):
        try:
            int(s, 16)
            datetime.utcfromtimestamp(int(s[:8], 16))
            assert str(s).lower() == str(s)
            assert len(s) is 24
        except (TypeError, ValueError, AssertionError):
            return False

        return True

    @classmethod
    def get_timestamp(cls, s):
        try:
            assert cls.is_valid(s)
        except AssertionError:
            return False
        else:
            return datetime.utcfromtimestamp(int(s[:8], 16))


from datetime import datetime

test.assert_equals(Mongo.is_valid(False), False)
test.assert_equals(Mongo.is_valid([]), False)
test.assert_equals(Mongo.is_valid(1234), False)
test.assert_equals(Mongo.is_valid('123476sd'), False)
test.assert_equals(Mongo.is_valid('507f1f77bcf86cd79943901'), False)
test.assert_equals(Mongo.is_valid('507f1f77bcf86cd799439016'), True)
test.assert_equals(Mongo.is_valid('507f1f77bcf86cd799439011'), True)
test.assert_equals(Mongo.is_valid('507f1f77bcf86cz799439011'), False)
test.assert_equals(Mongo.is_valid('507f1f77bcf86cd79943901'), False)
test.assert_equals(Mongo.is_valid('111111111111111111111111'), True)
test.assert_equals(Mongo.is_valid(111111111111111111111111), False)
test.assert_equals(Mongo.is_valid('507f1f77bcf86cD799439011'), False)

test.assert_equals(Mongo.get_timestamp(False), False)
test.assert_equals(Mongo.get_timestamp([]), False)
test.assert_equals(Mongo.get_timestamp(1234), False)
test.assert_equals(Mongo.get_timestamp('123476sd'), False)
test.assert_equals(Mongo.get_timestamp('507f1f77bcf86cd79943901'), False)
test.assert_equals(Mongo.get_timestamp('507f1f77bcf86cd799439016'),
                   datetime(2012, 10, 17, 21, 13, 27))
# Wed Oct 17 2012 21:13:27 GMT-0700 (Pacific Daylight Time)
test.assert_equals(Mongo.get_timestamp('507f1f77bcf86cd799439011'),
                   datetime(2012, 10, 17, 21, 13, 27))
test.assert_equals(Mongo.get_timestamp('507f1f77bcf86cz799439011'), False)
test.assert_equals(Mongo.get_timestamp('507f1f77bcf86cd79943901'), False)
# Sun Jan 28 1979 00:25:53 GMT-0800 (Pacific Standard Time)
test.assert_equals(Mongo.get_timestamp('111111111111111111111111'),
                   datetime(1979, 1, 28, 00, 25, 53))
test.assert_equals(Mongo.get_timestamp(111111111111111111111111), False)
