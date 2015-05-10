# Codewars-Katas

`skeleton` is my constantly evolving template.  I like to work in my IDE (pycharm) for practice.  This skeleton makes it copy and paste friendly.

Most important is the TestHandler class, this lets you run the test cases using codewars syntax.


##Notes

`test.expect_error()` does not work, yet.  This problem is harder to solve: it evaluates before it gets to the test handler OR if you try `eval()` on a string, it doesn't access to the rest of the page.  This creates a problem with setting up objects.

requires `from tabulate import tabulate` and `from termcolor import colored`

##usuage
 1) Copy and paste the skeleton, renaming it.

 2) Code AND test cases goes in `solution.py`

 3) `python skeleton/main.py`  of course using your folder name from step 1