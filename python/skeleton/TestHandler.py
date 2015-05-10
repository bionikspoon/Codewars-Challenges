from tabulate import tabulate
from termcolor import colored


class TestHandler(object):
    asserts_list = [("", "Act", "Exp", "Msg")]
    expect_list = [("", "Exp", "Msg")]
    expect_errors_list = [("", "Msg")]
    count = 0

    def assert_equals(self, actual, expected, message="{actual} should be {expected}"):
        message = message.format(actual=actual, expected=expected)
        try:
            assert actual == expected, message
        except AssertionError, e:
            self.handle_asserts(colored(" X", "red"), actual, expected, e)

        else:
            self.handle_asserts(colored("OK", "green"), actual, expected, message)

    def expect(self, expected, message="{expected} was expected"):
        message = message.format(expected=expected)

        try:
            assert expected is True, message
        except AssertionError, e:
            self.handle_expects(colored(" X", "red"), expected, e)
        else:
            self.handle_asserts(colored("OK", "green"), expected, message)

    def expect_error(self, message, thunk):  # TODO: does not work
        try:
            eval(thunk)
        except Exception as e:
            self.handle_expect_errors(colored("OK", "green"), e.message)
        else:
            self.handle_expect_errors(colored(" X", "white"), message)

    def describe(self, message):
        self.handle_all(colored(message.upper(), "blue", attrs=['bold', 'underline']))

    def it(self, message):
        self.handle_all(colored(message, "magenta"))

    def handle_asserts(self, summary=None, actual=None, expected=None, message=None):
        self.asserts_list.append((summary, actual, expected, message))

    def handle_expects(self, summary=None, test_bool=None, message=None):
        self.expect_list.append((summary, test_bool, message))

    def handle_expect_errors(self, summary=None, message=None):
        self.expect_errors_list.append((summary, message))

    def handle_all(self, message):
        TestHandler.count += 1
        self.handle_asserts(message=message)
        self.handle_expects(message=message)
        self.handle_expect_errors(message=message)

    def dispatch_asserts(self):
        if len(self.asserts_list) > (1 + TestHandler.count):
            print tabulate(self.asserts_list, headers="firstrow")
        if len(self.expect_list) > (1 + TestHandler.count):
            print tabulate(self.expect_list, headers="firstrow")
        if len(self.expect_errors_list) > (1 + TestHandler.count):
            print tabulate(self.expect_errors_list, headers="firstrow")