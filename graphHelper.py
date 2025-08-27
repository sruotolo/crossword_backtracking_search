import constants


class GraphHelper:
    # this class stores the information used to create result graphs

    def __init__(self):
        self.wordCSPTimes = self.createEmptyDictionary()
        self.letterCSPTime = self.createEmptyDictionary()
        self.found = dict()

    def createEmptyDictionary(self):
        emptyTimes = dict()

        for value in constants.CROSSWORD_GRID_DIMENSION.values():
            emptyTimes[value] = dict()

        for key in emptyTimes.keys():
            for length in constants.WORDS_LIST_LENGTH:
                emptyTimes[key][length] = []

        return emptyTimes
