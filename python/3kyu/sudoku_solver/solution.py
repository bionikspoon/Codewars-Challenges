from main import *


class SudokuSolver(object):
    DEBUG = False

    def __init__(self, puzzle):
        """
        Initialize with an unsolved puzzle.

        :param puzzle:
        :return:
        """
        self.puzzle = puzzle
        self.puzzle_range = set(xrange(9))
        self.puzzle_set = set(xrange(1, 10))
        self.DEBUG = False
        f = self.z_map_generator()
        self.z_map = {i: f.next() for i in self.puzzle_range}

    @staticmethod
    def z_map_generator():
        """
        Map mini boxes (dimension z) to coordinates.

        :return:
        """
        for col in xrange(3):
            for row in xrange(3):
                yield [(row * 3 + i, col * 3 + j) for j in xrange(3) for i in
                       xrange(3)]

    def get_z(self, coordinates):
        """
        Given coordinates, find z index.

        :param coordinates:
        :return:
        """
        return (k for k, v in self.z_map.items() if coordinates in v).next()

    def get_x_values_set(self, given_x):
        """
        Given x, return a set of values excluding 0.

        :param given_x:
        :return:
        """
        return {self.puzzle[y][given_x] for y in self.puzzle_range if
                self.puzzle[y][given_x] is not 0}

    def get_y_values_set(self, given_y):
        """
        Given y, return a set of values excluding 0.

        :param given_y:
        :return:
        """
        return {y for y in self.puzzle[given_y] if y is not 0}

    def get_z_values_set(self, get_z):
        """
        Given z, return a set of values excluding 0.

        :param get_z:
        :return:
        """
        return {self.puzzle[y][x] for x, y in self.z_map.get(get_z) if
                self.puzzle[y][x] is not 0}

    def get_possible_values(self, (x, y)):
        """
        Given coordinates, search x, y, z to infer all possible values.

        :return:
        """
        if self.puzzle[y][x] is not 0:
            return {self.puzzle[y][x]}
        z = self.get_z((x, y))
        return self.puzzle_set - (
            self.get_x_values_set(x) | self.get_y_values_set(
                y) | self.get_z_values_set(z))

    def get_zero_coordinates(self):
        """
        Return a set of coordinates where value is 0.

        :return:
        """
        return {(x, y) for x in self.puzzle_range for y in self.puzzle_range if
                self.puzzle[y][x] is 0}

    def search_one_possible(self, coordinates_set=None):
        """
        Given a set of coordinates, find all with only one possible solution.

        :param coordinates_set:
        :return:
        """
        if not coordinates_set:
            coordinates_set = self.get_zero_coordinates()
        return {(x, y): list(self.get_possible_values((x, y)))[0] for (x, y) in
                coordinates_set if len(self.get_possible_values((x, y))) is 1}

    def solution(self):
        """
        Solve the puzzle.

        :return:
        """
        while True:
            if self.DEBUG:
                print "-" * 10
            zero_coordinates = self.get_zero_coordinates()
            if len(zero_coordinates) is 0:
                return self.puzzle
            for (x, y), v in self.search_one_possible(zero_coordinates).items():
                self.puzzle[y][x] = v
                if self.DEBUG:
                    print "(%i, %i) is %i" % (x, y, v)


def sudoku(puzzle):
    """return the solved puzzle as a 2d array of 9 x 9"""

    solution = SudokuSolver(puzzle)
    return solution.solution()


puzzle = [[5, 3, 0, 0, 7, 0, 0, 0, 0], [6, 0, 0, 1, 9, 5, 0, 0, 0],
          [0, 9, 8, 0, 0, 0, 0, 6, 0], [8, 0, 0, 0, 6, 0, 0, 0, 3],
          [4, 0, 0, 8, 0, 3, 0, 0, 1], [7, 0, 0, 0, 2, 0, 0, 0, 6],
          [0, 6, 0, 0, 0, 0, 2, 8, 0], [0, 0, 0, 4, 1, 9, 0, 0, 5],
          [0, 0, 0, 0, 8, 0, 0, 7, 9]]
test_puzzle = SudokuSolver(puzzle)
test_puzzle_2 = SudokuSolver(puzzle)
test_puzzle.DEBUG = True

Test.it("Generates z_map on init")
test_z_map = {
    0: [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)],
    1: [(3, 0), (4, 0), (5, 0), (3, 1), (4, 1), (5, 1), (3, 2), (4, 2), (5, 2)],
    2: [(6, 0), (7, 0), (8, 0), (6, 1), (7, 1), (8, 1), (6, 2), (7, 2), (8, 2)],
    3: [(0, 3), (1, 3), (2, 3), (0, 4), (1, 4), (2, 4), (0, 5), (1, 5), (2, 5)],
    4: [(3, 3), (4, 3), (5, 3), (3, 4), (4, 4), (5, 4), (3, 5), (4, 5), (5, 5)],
    5: [(6, 3), (7, 3), (8, 3), (6, 4), (7, 4), (8, 4), (6, 5), (7, 5), (8, 5)],
    6: [(0, 6), (1, 6), (2, 6), (0, 7), (1, 7), (2, 7), (0, 8), (1, 8), (2, 8)],
    7: [(3, 6), (4, 6), (5, 6), (3, 7), (4, 7), (5, 7), (3, 8), (4, 8), (5, 8)],
    8: [(6, 6), (7, 6), (8, 6), (6, 7), (7, 7), (8, 7), (6, 8), (7, 8), (8, 8)]}

Test.assert_equals(test_puzzle.z_map, test_z_map)

Test.it("Returns Z given coordinates")
Test.assert_equals(test_puzzle.get_z((0, 0)), 0)
Test.assert_equals(test_puzzle.get_z((3, 1)), 1)
Test.assert_equals(test_puzzle.get_z((0, 3)), 3)
Test.assert_equals(test_puzzle.get_z((7, 8)), 8)

Test.it("Returns a set of values given X (excludes 0)")
Test.assert_equals(test_puzzle.get_x_values_set(0), {4, 5, 6, 7, 8})
Test.assert_equals(test_puzzle.get_x_values_set(3), {1, 4, 8})
Test.assert_equals(test_puzzle.get_x_values_set(8), {1, 3, 5, 6, 9})

Test.it("Returns a set of values given Y (excludes 0)")
Test.assert_equals(test_puzzle.get_y_values_set(0), {3, 5, 7})
Test.assert_equals(test_puzzle.get_y_values_set(3), {3, 6, 8})
Test.assert_equals(test_puzzle.get_y_values_set(8), {7, 8, 9})

Test.it("Returns a set of values given Z (excludes 0)")
Test.assert_equals(test_puzzle.get_z_values_set(0), {3, 5, 6, 8, 9})
Test.assert_equals(test_puzzle.get_z_values_set(4), {2, 3, 6, 8})

Test.it("Given a set of coordinates, it returns all possible values")
Test.assert_equals(test_puzzle.get_possible_values((0, 0)), {5})
Test.assert_equals(test_puzzle.get_possible_values((2, 0)), {1, 2, 4})
Test.assert_equals(test_puzzle.get_possible_values((4, 0)), {7})
Test.assert_equals(test_puzzle.get_possible_values((8, 6)), {4})

Test.it("Returns a set of coordinates with value == 0")
test_zero_coordinates = {(7, 3), (1, 3), (3, 0), (2, 8), (8, 0), (7, 7), (0, 7),
                         (5, 6), (6, 2), (2, 5), (5, 8), (8, 2), (7, 4), (6, 7),
                         (3, 3), (2, 0), (8, 1), (4, 4), (6, 3), (1, 5), (3, 6),
                         (8, 6), (5, 3), (1, 1), (6, 4), (3, 2), (2, 6), (5, 0),
                         (7, 1), (5, 5), (1, 4), (6, 0), (7, 5), (2, 3), (2, 1),
                         (6, 8), (4, 2), (0, 8), (6, 5), (3, 5), (2, 7), (7, 0),
                         (4, 6), (6, 1), (0, 2), (3, 8), (0, 6), (1, 8), (1, 7),
                         (5, 2), (2, 4)}
Test.assert_equals(test_puzzle.get_zero_coordinates(), test_zero_coordinates)

Test.it("It searches for coordinates with one possible solution")
test_one_possible_solution = {(5, 6): 7, (8, 6): 4, (4, 4): 5, (7, 7): 3}
Test.assert_equals(
    test_puzzle.search_one_possible(test_puzzle.get_zero_coordinates()),
    test_one_possible_solution)
Test.assert_equals(test_puzzle.search_one_possible(),
                   test_one_possible_solution)

Test.it("Solves the puzzle")
solution = [[5, 3, 4, 6, 7, 8, 9, 1, 2], [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7], [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1], [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4], [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]]
test.assert_equals(test_puzzle.solution(), solution)
test.assert_equals(test_puzzle_2.solution(), solution)

Test.describe('Sudoku')

Test.it('Puzzle 1')
Test.assert_equals(sudoku(puzzle), solution,
                   "Incorrect solution for the following puzzle: " + str(
                       puzzle))
