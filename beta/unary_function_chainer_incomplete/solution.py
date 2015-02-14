from main import test


def chained(functions):
    f = functions.pop()
    return f if not functions else lambda x: f(chained(functions)(x))


def f1(x): return x * 2


def f2(x): return x + 2


def f3(x): return x ** 2


def f4(x): return x.split()


def f5(xs): return [x[::-1].title() for x in xs]


def f6(xs): return "_".join(xs)


test.assert_equals(f3(f2(f1(0))), 4)

test.assert_equals(chained([f3])(0), f3(0))
test.assert_equals(chained([f2, f3])(1), f3(f2(1)))  # 9
test.assert_equals(chained([f2, f3])(0), f3(f2(0)))  # 4
test.assert_equals(chained([f1, f2, f3])(0), f3(f2(f1(0))))  # 4

test.assert_equals(chained([f1, f2, f3])(0), 4)
test.assert_equals(chained([f1, f2, f3])(2), 36)
test.assert_equals(chained([f3, f2, f1])(2), 12)

test.assert_equals(chained([f4, f5, f6])("lorem ipsum dolor"),
                   "Merol_Muspi_Rolod")

test.assert_equals(chained([f3, f2, f1, f1, f1, f1])(2), 96)


def left((x, y)):
    return (x - 1, y)


def right((x, y)):
    return (x + 1, y)


def up((x, y)):
    return (x, y + 1)


def down((x, y)):
    return (x, y - 1)


test.assert_equals(chained([left, left, up, left])((0, 0)), (-3, 1))