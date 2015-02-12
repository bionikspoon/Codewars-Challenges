from textwrap import wrap, fill
from tabulate import tabulate
from termcolor import colored


class TestHandler(object):
    asserts_list = [("", "Act", "Exp", "Msg")]
    expect_errors_list = [("", "Msg")]
    count = 0

    def assert_equals(self, actual, expected,
                      message="{actual} should be {expected}"):
        status_code = ""
        message = message.format(actual=actual, expected=expected)
        try:
            assert actual == expected, message
        except AssertionError, e:
            status_code = colored(" X", "red")
            message = e
        else:
            status_code = colored("OK", "green")
        finally:
            self.handle_asserts(status_code, str(actual)[:40],
                                str(expected)[:40], str(message)[:40])

    def expect(self, actual, message="{expected} was expected"):
        message = message.format(expected=actual)

        self.assert_equals(actual, True, message)

    def expect_error(self, message, thunk):  # TODO: does not work
        try:
            eval(thunk)
        except Exception as e:
            self.handle_expect_errors(colored("OK", "green"), e.message)
        else:
            self.handle_expect_errors(colored(" X", "white"), message)

    def describe(self, message):
        self.handle_all(
            colored(message.upper(), "blue", attrs=['bold', 'underline']))

    def it(self, message):
        self.handle_all(colored(message, "magenta"))

    def handle_asserts(self, summary=None, actual=None, expected=None,
                       message=None):
        self.asserts_list.append((summary, actual, expected, message))


    def handle_expect_errors(self, summary=None, message=None):
        self.expect_errors_list.append((summary, message))

    def handle_all(self, message):
        TestHandler.count += 1
        self.handle_asserts(message=message)
        self.handle_expect_errors(message=message)

    def dispatch_asserts(self):
        if len(self.asserts_list) > (1 + TestHandler.count):
            print tabulate(self.asserts_list, headers="firstrow")
        if len(self.expect_errors_list) > (1 + TestHandler.count):
            print tabulate(self.expect_errors_list, headers="firstrow")