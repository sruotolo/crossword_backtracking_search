import constants
import wordVariable
import uuid
from collections import defaultdict


class WordCrosswordProblem:
    # this class represents the constraint problem with variables represented as the word in the grid
    # it contains the list of words to be used to solve the problem, the grid, the variables and their domains and
    # a dictionary with a list of neighbors for every variable

    def __init__(self, grid, words):
        self.crosswordGrid = grid
        self.solution = []
        self.words = words
        self.variables = self.findVariables()
        self.domains = self.defineVariableDomain()
        self.constraints = self.defineConstraints()
        self.stepToSolve = 0

    def findVariables(self):
        # it finds all the variable in the grid, both horizontal and vertical variable
        # it uses createVariable to create the variable and puts all of them in self.variable

        variables = []
        for r, row in enumerate(self.crosswordGrid.grid):
            for c, col in enumerate(row):
                if (c == 0 or self.crosswordGrid.grid[r][c - 1] == '#') and (c < len(row) - 1 and
                                                                             self.crosswordGrid.grid[r][c + 1] == '_'):
                    variables.append(self.createVariable(r, c, constants.HORIZONTAL_DIRECTION))
                if ((r == 0 or self.crosswordGrid.grid[r - 1][c] == '#') and
                        (r < len(self.crosswordGrid.grid) - 1 and self.crosswordGrid.grid[r + 1][c] == '_')):
                    variables.append(self.createVariable(r, c, constants.VERTICAL_DIRECTION))

        noBlankVariables = []
        for var in variables:
            if len(var.cellsList) > 1:
                noBlankVariables.append(var)

        return noBlankVariables

    def createVariable(self, row, col, direction):
        # creates a variable from the starting cell (row, col) in the grid

        variableID = uuid.uuid4()
        cellsList = []
        if direction == constants.HORIZONTAL_DIRECTION:
            while col < len(self.crosswordGrid.grid[row]) and self.crosswordGrid.grid[row][col] == '_':
                cellsList.append((row, col))
                col += 1
            var = wordVariable.WordVariable(constants.HORIZONTAL_DIRECTION, cellsList, variableID)
        elif direction == constants.VERTICAL_DIRECTION:
            while row < len(self.crosswordGrid.grid) and self.crosswordGrid.grid[row][col] == '_':
                cellsList.append((row, col))
                row += 1
            var = wordVariable.WordVariable(constants.VERTICAL_DIRECTION, cellsList, variableID)

        return var

    def defineVariableDomain(self):
        # search in the list of words the words with the same length as the variable and save them
        # the chosen words are saved in a dictionary with key=variable and values=list of words (with same length)

        domains = defaultdict(list)
        for variable in self.variables:
            domains[variable] = []
            for word in self.words:
                if len(word) == variable.length:
                    if variable in domains.keys():
                        domains[variable].append(word)

        return domains

    def variablesOverlap(self, firstVar, secondVar):
        # verify if two variable overlap i.e. if both contain the same cell

        overlap = None

        for i, firstCell in enumerate(firstVar.cellsList):
            for j, secondCell in enumerate(secondVar.cellsList):
                if firstCell == secondCell:
                    overlap = (i, j)

        return overlap

    def defineConstraints(self):
        constraints = defaultdict(list)

        for var1 in self.variables:
            for var2 in self.variables:
                if var1 != var2:
                    overlap = self.variablesOverlap(var1, var2)
                    if overlap:
                        constraints[var1].append((var2, overlap))

        return constraints
