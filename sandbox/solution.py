from main import *

from datetime import datetime


class Mongo(object):
    @classmethod
    def is_valid(cls, s):
        """returns True if s is a valid MongoID; otherwise False"""
        return False

    @classmethod
    def get_timestamp(cls, s):
        """if s is a MongoID, returns a datetime object for the timestamp; otherwise False"""
        return False


from datetime import datetime

test.assert_equals(Mongo.is_valid(False), False)
test.assert_equals(Mongo.is_valid([]), False)
test.assert_equals(Mongo.is_valid(1234), False)
test.assert_equals(Mongo.is_valid('123476sd'), False)
test.assert_equals(Mongo.is_valid('507f1f77bcf86cd79943901'), False)
test.assert_equals(Mongo.is_valid('507f1f77bcf86cd799439016'), True)

test.assert_equals(Mongo.get_timestamp(False), False)
test.assert_equals(Mongo.get_timestamp([]), False)
test.assert_equals(Mongo.get_timestamp(1234), False)
test.assert_equals(Mongo.get_timestamp('123476sd'), False)
test.assert_equals(Mongo.get_timestamp('507f1f77bcf86cd79943901'), False)
test.assert_equals(Mongo.get_timestamp('507f1f77bcf86cd799439016'),
                   datetime(2012, 10, 17, 21, 13, 27))
