import string
from collections import defaultdict
import constants
import letterCSPConstraint


class LetterCrosswordProblem:
    # this class represents the constraint problem with variables represented as cells
    # it contains the list of words to be used to solve the problem, the grid, the variables and their domains and
    # a dictionary with a list of neighbors for every variable

    def __init__(self, grid, words):
        self.crosswordGrid = grid
        self.words = words
        self.variables = self.findVariables()
        self.domains = self.defineVariableDomain()
        self.constraints = self.findConstraints()
        self.stepToSolve = 0

    def findVariables(self):
        variables = []
        for row in range(self.crosswordGrid.rows):
            for col in range(self.crosswordGrid.columns):
                if self.crosswordGrid.grid[row][col] == '_':
                    var = (row, col)
                    variables.append(var)

        return variables

    def defineVariableDomain(self):
        domains = defaultdict(list)
        for var in self.variables:
            for letter in string.ascii_lowercase:
                domains[var].append(letter)

        return domains

    def findConstraints(self):
        # it finds all the constraints (sequence of blank cells) in the grid, both horizontal and vertical
        # it uses createConstraints to create the constraint and puts all of them in self.constraints

        constraints = []
        for r, row in enumerate(self.crosswordGrid.grid):
            for c, col in enumerate(row):
                if (c == 0 or self.crosswordGrid.grid[r][c - 1] == '#') and (c < len(row) - 1 and
                                                                             self.crosswordGrid.grid[r][c + 1] == '_'):
                    cellsList = self.createConstraints(r, c, constants.HORIZONTAL_DIRECTION)
                    if len(cellsList) > 1:
                        constraints.append(letterCSPConstraint.LetterCSPConstraint(cellsList, self.words))
                if ((r == 0 or self.crosswordGrid.grid[r - 1][c] == '#') and
                        (r < len(self.crosswordGrid.grid) - 1 and self.crosswordGrid.grid[r + 1][c] == '_')):
                    cellsList = self.createConstraints(r, c, constants.VERTICAL_DIRECTION)
                    if len(cellsList) > 1:
                        constraints.append(letterCSPConstraint.LetterCSPConstraint(cellsList, self.words))

        return constraints

    def createConstraints(self, row, col, direction):
        # creates a constraint from the starting cell (row, col) in the grid

        cellsList = []
        if direction == constants.HORIZONTAL_DIRECTION:
            while col < len(self.crosswordGrid.grid[row]) and self.crosswordGrid.grid[row][col] == '_':
                cellsList.append((row, col))
                col += 1
        elif direction == constants.VERTICAL_DIRECTION:
            while row < len(self.crosswordGrid.grid) and self.crosswordGrid.grid[row][col] == '_':
                cellsList.append((row, col))
                row += 1

        return cellsList
