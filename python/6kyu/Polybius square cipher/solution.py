from itertools import product
from main import *


cipher = {k: "".join(v) for k, v in zip("ABCDEFGHIKLMNOPQRSTUVWXYZ", product('12345', repeat=2))}
cipher['J'] = '24'
cipher[' '] = ' '


def polybius(text):
    result = "".join(cipher.get(c) for c in text)
    return result


Test.assert_equals(polybius('A'), '11', 'A')
Test.assert_equals(polybius('IJ'), '2424', 'IJ')
Test.assert_equals(polybius('CODEWARS'), '1334141552114243', 'CODEWARS')
Test.assert_equals(polybius('POLYBIUS SQUARE CIPHER'), '3534315412244543 434145114215 132435231542',
                   'POLYBIUS SQUARE CIPHER')