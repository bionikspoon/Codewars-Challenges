from main import test


def rgb(r, g, b):
    def rgb_print(i):
        i = min(255, max(0, i))
        return hex(i)[2:].zfill(2).upper()

    return "%s%s%s" % (rgb_print(r), rgb_print(g), rgb_print(b))


test.assert_equals(rgb(0, 0, 0), "000000", "testing zero values")
test.assert_equals(rgb(1, 2, 3), "010203", "testing near zero values")
test.assert_equals(rgb(255, 255, 255), "FFFFFF", "testing max values")
test.assert_equals(rgb(254, 253, 252), "FEFDFC", "testing near max values")
test.assert_equals(rgb(-20, 275, 125), "00FF7D", "testing out of range values")
test.assert_equals(rgb(255, 255, 300), "FFFFFF")
test.assert_equals(rgb(148, 0, 211), "9400D3")