from matplotlib import gridspec

import wordBacktrack
import letterBacktrack
import constants
import matplotlib.pyplot as plt


def buildWordsListFromFile(wordsPath):
    # build a list of words from a file (in this case a .txt file containing some italian words)

    words = []
    with open(wordsPath, "r", encoding="utf-8") as wordsFile:
        for word in wordsFile:
            words.append(word.rstrip())
    return words


def solveCrossword(csp):
    result, timeToResult = wordBacktrack.wordBacktrackingSearch(csp)
    if result:
        return result, round(timeToResult, 2)
    else:
        return False, round(timeToResult, 2)


def solveLetterCrossword(csp):
    result, timeToResult = letterBacktrack.letterBacktrackingSearch(csp)
    if result:
        return result, round(timeToResult, 2)
    else:
        return False, round(timeToResult, 2)


def printSolution(csp, solution, timeToResult):
    if solution is not False:
        gridIntoList = [list(gridList) for gridList in csp.crosswordGrid.grid]
        for var, word in solution.items():
            for i in range(var.length):
                if var.direction == constants.HORIZONTAL_DIRECTION:
                    gridIntoList[var.cellsList[0][0]][var.cellsList[0][1] + i] = word[i]
                elif var.direction == constants.VERTICAL_DIRECTION:
                    gridIntoList[var.cellsList[0][0] + i][var.cellsList[0][1]] = word[i]
        csp.solution = [''.join(row) for row in gridIntoList]

        with open(constants.SOLUTIONS_PATH, 'a') as file:
            file.write('Crossword dimensions: ' + str(csp.crosswordGrid.rows) + ' x ' + str(csp.crosswordGrid.columns)
                       + '\n')
            file.write('Number of words used: ' + str(len(csp.words)) + '\n')
            for row in csp.solution:
                file.write(''.join(row) + '\n')
            file.write('Time: ' + str(timeToResult))
            file.write('\n\n')

    else:
        with open(constants.SOLUTIONS_PATH, 'a') as file:
            file.write('Crossword dimensions: ' + str(csp.crosswordGrid.rows) + ' x ' + str(csp.crosswordGrid.columns)
                       + '\n')
            file.write('Number of words used: ' + str(len(csp.words)) + '\n')
            file.write('No solution found with the words set given' + '\n')
            file.write('Time: ' + str(timeToResult))
            file.write('\n\n')


def printLetterSolution(csp, solution, timeToResult):
    if solution is not False:
        gridIntoList = [list(gridList) for gridList in csp.crosswordGrid.grid]
        for var, value in solution.items():
            gridIntoList[var[0]][var[1]] = value

        with open(constants.LETTER_SOLUTIONS_PATH, 'a') as file:
            file.write('Crossword dimensions: ' + str(csp.crosswordGrid.rows) + ' x ' + str(csp.crosswordGrid.columns)
                       + '\n')
            file.write('Number of words used: ' + str(len(csp.words)) + '\n')
            for row in gridIntoList:
                file.write(''.join(row) + '\n')
            file.write('Time: ' + str(timeToResult))
            file.write('\n\n')

    else:
        with open(constants.LETTER_SOLUTIONS_PATH, 'a') as file:
            file.write('Crossword dimensions: ' + str(csp.crosswordGrid.rows) + ' x ' + str(csp.crosswordGrid.columns)
                       + '\n')
            file.write('Number of words used: ' + str(len(csp.words)) + '\n')
            file.write('No solution found with the words set given' + '\n')
            file.write('Time: ' + str(timeToResult))
            file.write('\n\n')


def createCSPGraphs(graphHelper):
    figure = plt.figure(None, (15, 17))
    gs = gridspec.GridSpec(constants.GRAPH_FIGURE_ROWS, constants.GRAPH_FIGURE_COL)

    gsPosX, gsPosY = 0, 0

    for crosswordSize in constants.CROSSWORD_GRID_DIMENSION.values():
        for wordsListLength in constants.WORDS_LIST_LENGTH:
            subPlot = figure.add_subplot(gs[gsPosX, gsPosY])
            subPlot.plot(range(1, constants.GRID_COUNTER + 1), graphHelper.wordCSPTimes[crosswordSize][wordsListLength],
                         label='Word CSP')
            subPlot.plot(range(1, constants.GRID_COUNTER + 1), graphHelper.letterCSPTime[crosswordSize][wordsListLength]
                         , label='Letter CSP')
            subPlot.set_title(f'Time to solve {crosswordSize} crossword with {wordsListLength} words')
            subPlot.set_xlabel('Crossword')
            subPlot.set_ylabel('Time (s)')

            subPlot.legend()

            gsPosY += 1
            if gsPosY >= constants.GRAPH_FIGURE_COL:
                gsPosY = 0
                gsPosX += 1

    subPlot = figure.add_subplot(gs[constants.GRAPH_FIGURE_ROWS - 1, int(constants.GRAPH_FIGURE_COL / 2)])
    subPlot.bar(['Word CSP', 'Letter CSP'], graphHelper.found.values())
    subPlot.set_title('Solutions founded')

    plt.tight_layout()

    plt.savefig('Results')
    figure.clf()
