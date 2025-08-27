import constants
import letterCrosswordProblem
import test
import gridDataset
import wordCrosswordProblem
import graphHelper

wordsList = []
for path in constants.WORDS_PATH:
    wordsList.append(test.buildWordsListFromFile(path))

gridDataset = gridDataset.GridDataset()

graphHelper = graphHelper.GraphHelper()

wordCspList = []
for key in gridDataset.dataSet.keys():
    for crossword in gridDataset.dataSet[key]:
        for wl in wordsList:
            wordCspList.append(wordCrosswordProblem.WordCrosswordProblem(crossword, wl))

wordCSPResultFound = 0
for csp in wordCspList:
    result, timeToResult = test.solveCrossword(csp)

    if len(graphHelper.wordCSPTimes[(csp.crosswordGrid.rows, csp.crosswordGrid.columns)][len(csp.words)]) == 0:
        graphHelper.wordCSPTimes[(csp.crosswordGrid.rows, csp.crosswordGrid.columns)][len(csp.words)] = [timeToResult]
    else:
        graphHelper.wordCSPTimes[(csp.crosswordGrid.rows, csp.crosswordGrid.columns)][len(csp.words)].append(timeToResult)
    
    if result:
        wordCSPResultFound += 1
    
    test.printSolution(csp, result, timeToResult)

if 'wordCSPResultFound' not in graphHelper.found.keys():
    graphHelper.found['wordCSPResultFound'] = wordCSPResultFound

letterCspList = []
for key in gridDataset.dataSet.keys():
    for crossword in gridDataset.dataSet[key]:
        for wl in wordsList:
            letterCspList.append(letterCrosswordProblem.LetterCrosswordProblem(crossword, wl))

letterCSPResultFound = 0
for letterCsp in letterCspList:
    result, timeToResult = test.solveLetterCrossword(letterCsp)
    
    if len((graphHelper.letterCSPTime[(letterCsp.crosswordGrid.rows, letterCsp.crosswordGrid.columns)][len(letterCsp.words)])) == 0:
        graphHelper.letterCSPTime[(letterCsp.crosswordGrid.rows, letterCsp.crosswordGrid.columns)][len(letterCsp.words)] = [timeToResult]
    else:
        graphHelper.letterCSPTime[(letterCsp.crosswordGrid.rows, letterCsp.crosswordGrid.columns)][len(letterCsp.words)].append(timeToResult)
    
    if result:
        letterCSPResultFound += 1
    
    test.printLetterSolution(letterCsp, result, timeToResult)

if 'letterCSPResultFound' not in graphHelper.found.keys():
    graphHelper.found['letterCSPResultFound'] = letterCSPResultFound

test.createCSPGraphs(graphHelper)
