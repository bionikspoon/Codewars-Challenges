#Test cases and notes:

My approach was to find the total possible anagrams per word and find the answer based on a simple fraction scoring system.

I wrote a helper function to find the possible number of arrangements: `number_of_arrangements`

I didn't know what the math was going to look like to get this number.  For discovery I used the permutations generator in a set to find out.  I had something like this:

```python
def number_of_arrangements(word):
    from itertools import permutations

    results = len({i for i in permutations(word)})
    print results
```

I knew this wouldn't be the final solution.  As a generator it has the O^2 problem. But this helped to get the following test cases:
```python
test.assert_equals(number_of_arrangements("AAA"), 1)
test.assert_equals(number_of_arrangements("AAB"), 3)
test.assert_equals(number_of_arrangements("ABB"), 3)  # 3*1*1
test.assert_equals(number_of_arrangements("ABC"), 6)  # 3*2*1
test.assert_equals(number_of_arrangements("AAAB"), 4)  # 4
test.assert_equals(number_of_arrangements("AABC"), 12)  # 4*3*1*1
test.assert_equals(number_of_arrangements("ABCD"), 24)  # 4*3*2*1
test.assert_equals(number_of_arrangements("AABB"), 6)  #
test.assert_equals(number_of_arrangements("AAAAB"), 5)  # 5
test.assert_equals(number_of_arrangements("AAABC"), 20)  # 5*4
test.assert_equals(number_of_arrangements("AABCD"), 60)  # 5*4*3
test.assert_equals(number_of_arrangements("ABCDE"), 120)  # 5*4*3*2*1
test.assert_equals(number_of_arrangements("AAABB"), 10)  # 5*2
test.assert_equals(number_of_arrangements("AABBC"), 30)  # 5*3*2
test.assert_equals(number_of_arrangements("ABBBC"), 20)  # 5*4
```


Initially, I didn't understand the math, but I knew factorials were involved, so I wrote out the answers in factorial form. e.g.:

```python
number_of_arrangements("ABCDE") == 120 # 5*4*3*2
number_of_arrangements("AABCD") ==  60 # 5*4*3
number_of_arrangements("AABBC") ==  30 # 5  *3*2
```

After about 15 of these I understood the pattern. You group and count the non-unique digits.  Then you divide the main factorial by the factorials of those counts.

so for

```python
number_of_arrangements("AABBC") ==  30
# instead of 5*3*2 it's better represented as
# FAC(5) / (FAC(2) * FAC(2) * FAC(1))
# 5*4*3*2*1 / 2*1*2*1*1 == 5*4*3*2/2*2
```

After I rewrote this helper function I added the following test to see if I solved the O^2 problem:

```python
# refactored helper function
def number_of_arrangements(word):
    letter_counts = [factorial(word.count(i)) for i in set(word)]
    return factorial(len(word)) / reduce(mul, letter_counts)

# 0^2 test
test.assert_equals(number_of_arrangements("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
                   403291461126605635584000000)
```

If your computer freezes, then you didn't pass.  :D  The `math.factorial()` function is lightning fast.

##My final test cases:

```python
test.assert_equals(number_of_arrangements("AAA"), 1)
test.assert_equals(number_of_arrangements("AAB"), 3)
test.assert_equals(number_of_arrangements("ABB"), 3)  # 3*1*1
test.assert_equals(number_of_arrangements("ABC"), 6)  # 3*2*1
test.assert_equals(number_of_arrangements("AAAB"), 4)  # 4
test.assert_equals(number_of_arrangements("AABC"), 12)  # 4*3*1*1
test.assert_equals(number_of_arrangements("ABCD"), 24)  # 4*3*2*1
test.assert_equals(number_of_arrangements("AABB"), 6)  #
test.assert_equals(number_of_arrangements("AAAAB"), 5)  # 5
test.assert_equals(number_of_arrangements("AAABC"), 20)  # 5*4

# 5*4*3*2*1/(3*2*1*2*1) == factorial(5)/factorial(2)
test.assert_equals(number_of_arrangements("AABCD"), 60)
test.assert_equals(number_of_arrangements("ABCDE"), 120)  # 5*4*3*2*1

# 5*4*3*2*1/(3*2*1*2*1) == factorial(5)/(factorial(3)*factorial(2))
test.assert_equals(number_of_arrangements("AAABB"), 10)

# 5*4*3*2*1/(2*1*2*1*1) == factorial(5)/(factorial(2)*factorial(2))
test.assert_equals(number_of_arrangements("AABBC"), 30)
test.assert_equals(number_of_arrangements("ABBBC"), 20)  # 5*2*3
test.assert_equals(number_of_arrangements("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
                   403291461126605635584000000)

test.describe('Anagram')
test.it('Must return appropriate values for known inputs')
testValues = {'A': 1, 'ABAB': 2, 'AAAB': 1, 'BAAA': 4, 'QUESTION': 24572,
              'BOOKKEEPER': 10743}
for word in testValues:
    test.assert_equals(listPosition(word), testValues[word],
                       'Incorrect list position for: ' + word)
```

##Scoring
The scoring system based on fractions of the possible solutions was mostly trial and error.  But I was comfortable with with the test cases that the author provided.  So I didn't add any there.