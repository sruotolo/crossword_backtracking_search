import re


class LetterCSPConstraint:
    # it represents a constraint in the CSP
    # it's used to check, after every assignment for a variable, if the words created in the grid are correct:
    # a word (i.e. all the letters in a constraint in order) is correct if it matches, considering both blank cells and
    # cells with a letter, at least a word in the dictionary (the blank cells are represented in the constraint as '.')

    def __init__(self, involvedVariables, words):
        self.involvedVariables = self.defineInvolvedVariables(involvedVariables)
        self.allowedWords = self.createAllowedWords(words)

    def defineInvolvedVariables(self, variables):
        # initialize every variable in the constraint with all blank cells

        involvedVariablesDictionary = {}

        for var in variables:
            if var not in involvedVariablesDictionary.keys():
                involvedVariablesDictionary[var] = '.'

        return involvedVariablesDictionary

    def createAllowedWords(self, words):
        # store in the constraint the words from the words list given that match the length of the constraint

        allowedWords = []
        for word in words:
            if len(word) == len(self.involvedVariables.keys()):
                allowedWords.append(word)

        return allowedWords

    def isSatisfied(self, assignment):
        pattern = self.extractWord(assignment)

        return any(re.match(pattern, word) for word in self.allowedWords)


    def extractWord(self, assignment):
        # creates a string representing the word created by the cells of the constraint
        # and then it restores the cells to all '.'

        for var in assignment:
            if var in self.involvedVariables.keys():
                self.involvedVariables[var] = assignment[var]

        word = ''
        for value in self.involvedVariables.values():
            word += value

        for var in self.involvedVariables.keys():
            if self.involvedVariables[var] != '.':
                self.involvedVariables[var] = '.'

        return word
