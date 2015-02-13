from main import test
from random import choice
from collections import deque


class BefungeInterpreter(object):
    def __init__(self, code, start_compiler=True):
        self._queue = deque()
        self._code = code
        self._direction = ">"
        self._pointer = (0, 0)
        self._code_map = self._generate_code_map()
        self._output = []
        self._string_mode = False
        if start_compiler: self._compile()

    def next(self):
        """
        Run current command, advance pointer.

        :return:
        """
        command = self._code_map.get(self._pointer)
        self._execute(command)
        self._pointer = self._next_step()

    def _compile(self):
        """
        Run code.

        :return:
        """
        while True:
            try:
                self.next()
            except StopIteration:
                break

    def _generate_code_map(self):
        """
        Map code to coordinates.

        :return:
        """
        x, y, result = 0, 0, {}
        for k, v in enumerate(self._code):
            if self._code[k:k + 1] == "\n":
                y += 1
                x = 0
            else:
                result[(x, y)] = v
                x += 1
        return result

    def _next_step(self, direction=None):
        """
        Given a direction and coordinates, find the location of the next step.

        :param direction:
        :return:
        """
        if direction is None: direction = self._direction
        (x, y) = self._pointer
        max_x = max([_x for _x, _y in self._code_map.keys() if _y == y])
        max_y = max([_y for _x, _y in self._code_map.keys() if _x == x])

        def right(x, y):
            if x == max_x:
                x = 0
                y += 1
                y = 0 if y > max_y else y
            else:
                x += 1

            return x, y

        def left(x, y):
            if x == 0:
                x = max_x
                y -= 1
                y = max_y if y < 0 else y
            else:
                x -= 1

            return x, y

        def down(x, y):
            if y == max_y:
                y = 0
                x += 1
                x = 0 if x > max_x else x
            else:
                y += 1
            return x, y

        def up(x, y):
            if y == 0:
                y = max_y
                x -= 1
                x = max_x if x < 0 else x
            else:
                y -= 1
            return x, y

        operation = {">": right, "v": down, "<": left, "^": up}

        self._pointer = operation[direction](x, y)
        return self._pointer

    def __str__(self):
        """
        Return object as string.

        :return:
        """
        output = self._output
        if not output:
            return ""
        output = map(str, output)
        return "".join(output)

    def _execute(self, command):
        """
        Execute command at current pointer.

        :param command:
        :return:
        """

        def push_value(_):
            self._queue.append(int(command))

        def math(command):
            a = int(self._queue.pop())
            b = int(self._queue.pop())

            if command == "+":
                self._queue.append(a + b)
            if command == "-":
                self._queue.append(b - a)
            if command == "*":
                self._queue.append(a * b)
            if command == "/":
                result = 0 if a is 0 else b // a
                self._queue.append(result)
            if command == "%":
                result = 0 if a is 0 else b % a
                self._queue.append(result)
            if command == "`":
                result = 1 if b > a else 0
                self._queue.append(result)

        def direction(_):
            self._direction = choice(
                [">", "v", "<", "^"]) if command == "?" else command

        def logical_not(_):
            result = self._queue.pop()
            result = 1 if result == 0 else 0
            self._queue.append(result)

        def pop_move(command):
            value = self._queue.pop()
            if command == "_":
                if value == 0:
                    self._direction = ">"
                else:
                    self._direction = "<"

            if command == "|":
                if value == 0:
                    self._direction = "v"

                else:
                    self._direction = "^"

        def string_mode_toggle(_):
            self._string_mode = True if self._string_mode is False else False

        def string_push(_):
            self._queue.append(ord(command))

        def duplicate_top(_):
            if len(self._queue) > 0:
                value = self._queue[-1]
                self._queue.append(value)
            else:
                self._queue.append(0)

        def swap_top(_):
            if len(self._queue) < 2:
                self._queue.appendleft(0)
            a = self._queue.pop()
            b = self._queue.pop()
            self._queue.append(a)
            self._queue.append(b)

        def pop_value(command):
            value = self._queue.pop()
            if command == ".":
                self._output.append(int(value))
            if command == ",":
                self._output.append(chr(value))

        def trampoline(_):
            self._next_step()

        def storage(command):
            y = int(self._queue.pop())
            x = int(self._queue.pop())
            if command == "p":
                v = int(self._queue.pop())
                self._code_map[(x, y)] = chr(v)
            if command == "g":
                character = ord(self._code_map.get((x, y)))
                self._queue.append(character)

        def end(_):
            raise StopIteration

        def skip(_):
            pass

        if self._string_mode and command != "\"":
            string_push(command)
        else:
            commands_dict = {"0": push_value, "1": push_value, "2": push_value,
                             "3": push_value, "4": push_value, "5": push_value,
                             "6": push_value, "7": push_value, "8": push_value,
                             "9": push_value, "+": math, "-": math, "*": math,
                             "/": math, "%": math, "!": logical_not, "`": math,
                             ">": direction, "<": direction, "^": direction,
                             "v": direction, "?": direction, "_": pop_move,
                             "|": pop_move, "\"": string_mode_toggle,
                             ":": duplicate_top, "\\": swap_top, "$": pop_value,
                             ".": pop_value, ",": pop_value, "#": trampoline,
                             "p": storage, "g": storage, "@": end, " ": skip}
            commands_dict[command](command)


def interpret(code):
    interpreter = BefungeInterpreter(code)
    return str(interpreter)


test.it("Builds a code map on init")
test_code = "123\n" \
            "456\n" \
            "78@"
test_interpreter_1 = BefungeInterpreter(test_code, start_compiler=False)
test_code_map = {(0, 0): '1', (1, 0): '2', (2, 0): '3', (0, 1): '4',
                 (1, 1): '5', (2, 1): '6', (0, 2): '7', (1, 2): '8',
                 (2, 2): '@'}

test.assert_equals(test_interpreter_1._code_map, test_code_map)

test_code = "12a\n" \
            "4 *\n" \
            " \@"
test_interpreter_2 = BefungeInterpreter(test_code, start_compiler=False)
test_code_map = {(0, 0): '1', (1, 0): '2', (2, 0): 'a', (0, 1): '4',
                 (1, 1): ' ', (2, 1): '*', (0, 2): ' ', (1, 2): '\\',
                 (2, 2): '@'}

test.assert_equals(test_interpreter_2._code_map, test_code_map)
del test_code_map

test.it("It finds the coordinates of the next step")
test.assert_equals(test_interpreter_1._next_step(), (1, 0))
test.assert_equals(test_interpreter_1._next_step(direction="<"), (0, 0))
test.assert_equals(test_interpreter_1._next_step(direction="<"), (2, 2))
test.assert_equals(test_interpreter_1._next_step(direction="<"), (1, 2))
test.assert_equals(test_interpreter_1._next_step(direction="v"), (2, 0))
test.assert_equals(test_interpreter_1._next_step(direction="v"), (2, 1))
test.assert_equals(test_interpreter_1._next_step(direction="v"), (2, 2))
test.assert_equals(test_interpreter_1._next_step(direction="v"), (0, 0))
test.assert_equals(test_interpreter_1._next_step(direction="^"), (2, 2))
test.assert_equals(test_interpreter_1._next_step(direction="^"), (2, 1))
test.assert_equals(test_interpreter_1._next_step(direction="^"), (2, 0))
test.assert_equals(test_interpreter_1._next_step(direction="^"), (1, 2))
test.assert_equals(test_interpreter_1._next_step(direction="v"), (2, 0))
test.assert_equals(test_interpreter_1._next_step(direction=">"), (0, 1))
test.assert_equals(test_interpreter_1._next_step(direction="^"), (0, 0))

test.it("It executes commands: direction")
test_code = ">>v\n" \
            ">@?\n" \
            "^<<"
test_interpreter_3 = BefungeInterpreter(test_code, start_compiler=False)
test_interpreter_3.next()
test_interpreter_3.next()
test.assert_equals(test_interpreter_3._pointer, (2, 0))
test_interpreter_3.next()
test.assert_equals(test_interpreter_3._direction, "v")
test_interpreter_3.next()

del test_interpreter_1
del test_interpreter_2
del test_interpreter_3

test.describe("Execute Commands")
test.it("push")
test_code = "132@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([1, 3, 2]))

test.it("math")
test_code = "12-@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([-1]))

test_code = "12+@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([3]))

test_code = "46*@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([24]))

test_code = "74695*@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([7, 4, 6, 45]))

test_code = "10/@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([0]))

test_code = "01/@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([0]))

test_code = "92/@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([4]))

test_code = "93/@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([3]))

test_code = "93%@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([0]))

test_code = "92%@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([1]))

test_code = "97%@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([2]))

test_code = "20%@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([0]))

test_code = "07%@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([0]))

test_code = "32`@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([1]))

test_code = "59`@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([0]))

test_code = "55`@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([0]))

test_code = "0!@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([1]))

test_code = "1!@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([0]))

test_code = "2!@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([0]))

test.it("direction")
test_code = "@"
test_commands = BefungeInterpreter(test_code, start_compiler=False)
test_commands._execute("<")
test.assert_equals(test_commands._direction, "<")
test_commands._execute("<")
test.assert_equals(test_commands._direction, "<")
test_commands._execute(">")
test.assert_equals(test_commands._direction, ">")
test_commands._execute("^")
test.assert_equals(test_commands._direction, "^")
test_commands._execute("v")
test.assert_equals(test_commands._direction, "v")

test.it("pop move")
test_code = "@"
test_commands = BefungeInterpreter(test_code, start_compiler=False)
test_commands._queue.append(1)
test_commands._execute("_")
test.assert_equals(test_commands._direction, "<")
test_commands._queue.append(0)
test_commands._execute("_")
test.assert_equals(test_commands._direction, ">")
test_commands._queue.append(0)
test_commands._execute("|")
test.assert_equals(test_commands._direction, "v")
test_commands._queue.append(1)
test_commands._execute("|")
test.assert_equals(test_commands._direction, "^")

test_code = "0 v  \n" \
            "@3_4@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([4]))
test_code = "1 v  \n" \
            "@3_4@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([3]))

test_code = 'v >3@\n' \
            '>0|  \n' \
            '  >4@'
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([4]))

test_code = 'v >3@\n' \
            '>1|  \n' \
            '  >4@'
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([3]))

test.it("string mode")
test_code = "@"
test_commands = BefungeInterpreter(test_code, start_compiler=False)
test.assert_equals(test_commands._string_mode, False)
test_commands._execute("\"")
test.assert_equals(test_commands._string_mode, True)
test_commands._execute("\"")
test.assert_equals(test_commands._string_mode, False)

test_code = '"Test"@'
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([84, 101, 115, 116]))

test.it("duplicates value on top of the stack")
test_code = "@"
test_commands = BefungeInterpreter(test_code, start_compiler=False)
test_commands._queue.append(1)
test_commands._execute(":")
test.assert_equals(test_commands._queue, deque([1, 1]))

test_code = "@"
test_commands = BefungeInterpreter(test_code, start_compiler=False)
test_commands._execute(":")
test.assert_equals(test_commands._queue, deque([0]))

test_code = "@"
test_commands = BefungeInterpreter(test_code, start_compiler=False)
test_commands._queue.append(1)
test_commands._queue.append(2)
test_commands._execute(":")
test.assert_equals(test_commands._queue, deque([1, 2, 2]))

test_code = "1:@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([1, 1]))

test_code = ":@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([0]))

test_code = "12:@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([1, 2, 2]))

test.it("Swaps top 2 values")
test_code = "@"
test_commands = BefungeInterpreter(test_code, start_compiler=False)
test_commands._queue.append(1)
test_commands._queue.append(2)
test.assert_equals(test_commands._queue, deque([1, 2]))
test_commands._execute("\\")
test.assert_equals(test_commands._queue, deque([2, 1]))

test_commands = BefungeInterpreter(test_code, start_compiler=False)
test_commands._queue.append(1)
test.assert_equals(test_commands._queue, deque([1]))
test_commands._execute("\\")
test.assert_equals(test_commands._queue, deque([1, 0]))

test_code = "@"
test_commands = BefungeInterpreter(test_code, start_compiler=False)
test_commands._queue.append(1)
test_commands._queue.append(2)
test_commands._queue.append(3)
test_commands._queue.append(4)
test_commands._queue.append(5)
test_commands._execute("\\")
test.assert_equals(test_commands._queue, deque([1, 2, 3, 5, 4]))

test_code = "12\@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([2, 1]))

test_code = "1\@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([1, 0]))

test_code = "12345\@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([1, 2, 3, 5, 4]))

test.it("pops values")
test_code = "1$@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([]))
test.assert_equals(test_commands._output, [])
test_code = "12345$$$@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([1, 2]))
test.assert_equals(test_commands._output, [])
test_code = "1.@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([]))
test.assert_equals(test_commands._output, [1])
test_code = "12345...@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([1, 2]))
test.assert_equals(test_commands._output, [5, 4, 3])

test_code = "@"
test_commands = BefungeInterpreter(test_code, start_compiler=False)
test_commands._queue.append(53)
test_commands._execute(",")
test.assert_equals(test_commands._queue, deque([]))
test.assert_equals(test_commands._output, ['5'])

test_code = "@"
test_commands = BefungeInterpreter(test_code, start_compiler=False)
test_commands._queue.append(49)
test_commands._queue.append(50)
test_commands._queue.append(51)
test_commands._queue.append(52)
test_commands._queue.append(53)
test_commands._execute(",")
test_commands._execute(",")
test_commands._execute(",")
test.assert_equals(test_commands._queue, deque([49, 50]))
test.assert_equals(test_commands._output, ['5', '4', '3'])

test_code = "96*5-,@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([]))
test.assert_equals(test_commands._output, ['1'])

test_code = "96*5-96*4-96*3-96*2-96*1-,,,@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([49, 50]))
test.assert_equals(test_commands._output, ['5', '4', '3'])

test.it("trampoline")
test_code = "#1@"
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([]))
test_code = ' v\n' \
            ' #\n' \
            ' 1\n' \
            ' 2\n' \
            ' @'
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([2]))
test_code = '#@v\n' \
            ' 3#\n' \
            ' 21\n' \
            ' # \n' \
            ' ^<'
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([3]))
test_code = '#1#@ #2# #5<'
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([5]))

test.it("gets and puts")
test_code = " @"
test_commands = BefungeInterpreter(test_code, start_compiler=False)
test_commands._queue.append(49)
test_commands._queue.append(0)
test_commands._queue.append(0)
test.assert_equals(test_commands._code_map.get((0, 0)), ' ')
test_commands._execute("p")
test.assert_equals(test_commands._queue, deque([]))
test.assert_equals(test_commands._code_map.get((0, 0)), '1')

test_code = " @"
test_commands = BefungeInterpreter(test_code, start_compiler=False)
test_commands._queue.append(118)
test_commands._queue.append(1)
test_commands._queue.append(2)
test_commands._execute("p")
test.assert_equals(test_commands._queue, deque([]))
test.assert_equals(test_commands._code_map.get((1, 2)), 'v')

test_code = '#@96*5-12pv\n' \
            '           \n' \
            ' 2         \n' \
            ' ^        <'
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._code_map.get((1, 2)), '1')
test.assert_equals(test_commands._queue, deque([1]))

test_code = '#210g@'
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([50]))

test_code = '34g@\n' \
            '    \n' \
            '    \n' \
            '    \n' \
            '   z'
test_commands = BefungeInterpreter(test_code)
test.assert_equals(test_commands._queue, deque([122]))

test.it("Converts output to string")
test_code = '"!olleH",,,,,,@'
test_commands = BefungeInterpreter(test_code)
test.assert_equals(str(test_commands), "Hello!")
del test_commands

test.describe("Sample Programs")
test_code = '"!olleH",,,,,,@'
test.assert_equals(interpret(test_code), "Hello!")

test_code = '>987v>.v\n' \
            'v456<  :\n' \
            '>321 ^ _@'
test.assert_equals(interpret(test_code), '123456789')

test_code = '>              v\n' \
            'v  ,,,,,"Hello"<\n' \
            '>48*,          v\n' \
            'v,,,,,,"World!"<\n' \
            '>25*,@'

test.assert_equals(interpret(test_code), 'Hello World!\n', "Hello World!")

test_code = '>25*"!dlrow ,olleH":v \n' \
            '                 v:,_@\n' \
            '                 >  ^ '
test.assert_equals(interpret(test_code), 'Hello, world!\n', "Hello, world!")

test_code = '0"!dlroW ,olleH">:#,_@'
test.assert_equals(interpret(test_code), 'Hello, World!')

test_code = '01->1# +# :# 0# g# ,# :# 5# 8# *# 4# +# -# _@'
test.assert_equals(interpret(test_code), test_code)

test_code = '08>:1-:v v *_$.@\n' \
            '  ^    _$>\:^'
test.assert_equals(interpret(test_code), '40320')