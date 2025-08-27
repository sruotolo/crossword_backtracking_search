import copy
import time
from collections import deque

import constants


def letterBacktrackingSearch(csp):
    result = None

    startTime = time.time()
    if ac3(csp, {}):
        result = letterBacktrack(csp, {})
    endTime = time.time()

    print(csp.stepToSolve)

    return result, endTime - startTime


def letterBacktrack(csp, assignment):
    if len(assignment) == len(csp.variables):
        return assignment
    if csp.stepToSolve <= constants.MAX_STEP:
        var = selectUnassignedVariable(csp, assignment)
        for value in orderDomainsValues(csp, var, assignment):
            if value is not None:
                csp.stepToSolve += 1
                print("Trying value", value, "for variable", var)
                if isConsistent(csp, var, value, assignment):
                    assignment[var] = value
                    oldDomains = copy.deepcopy(csp.domains)
                    csp.domains[var] = value
                    inference = doInference(csp, assignment)
                    if inference:
                        result = letterBacktrack(csp, assignment)
                        if result:
                            return result
                    del assignment[var]
                    csp.domains = oldDomains

    return False


def doInference(csp, assignment):
    return ac3(csp, assignment)


def ac3(csp, assignment):
    queue = deque()

    for xi in csp.variables:
        for constraint in csp.constraints:
            if xi in constraint.involvedVariables.keys():
                for xj in constraint.involvedVariables.keys():
                    if xi != xj:
                        queue.append((xi, xj))

    while queue:
        (xi, xj) = queue.popleft()
        if revise(csp, xi, xj, assignment):
            if not csp.domains[xi]:
                return False
            for xk in csp.constraints[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True


def revise(csp, xi, xj, assignment):
    revised = False

    for valueX in csp.domains[xi]:
        if all(not isConsistent(csp, xj, valueY, assignment) for valueY in csp.domains[xj]):
            csp.domains[xi] = [val for val in csp.domains[xi] if val != valueX]
            revised = True

    return revised


def isConsistent(csp, var, value, assignment):
    tempAssignment = copy.deepcopy(assignment)
    tempAssignment[var] = value

    consistent = True

    if not all(constraint.isSatisfied(tempAssignment) for constraint in csp.constraints):
        consistent = False

    completedWords = []
    for constraint in csp.constraints:
        word = constraint.extractWord(tempAssignment)
        if len(word) == len(constraint.involvedVariables) and '.' not in word:
            completedWords.append(word)

    if len(set(completedWords)) != len(completedWords):
        consistent = False

    return consistent


def orderDomainsValues(csp, var, assignment):
    # use the number of conflicts to order the values according to the LCV heuristic

    return sorted(csp.domains[var], key=lambda val: countConflicts(csp, var, val, assignment))


def countConflicts(csp, var, value, assignment):
    conflicts = 0
    tempAssignment = copy.deepcopy(assignment)
    tempAssignment[var] = value

    for constraint in csp.constraints:
        if var in constraint.involvedVariables:
            for otherVar in constraint.involvedVariables:
                if otherVar != var and otherVar not in assignment:
                    for otherValue in csp.domains[otherVar]:
                        tempAssignment[otherVar] = otherValue
                        if not constraint.isSatisfied(tempAssignment):
                            conflicts += 1
                        del tempAssignment[otherVar]

    return conflicts


def selectUnassignedVariable(csp, assignment):
    # choose the variable to assign according to the heuristic MRV (minimum remaining variables):
    # it chooses the variable which domain is the smallest

    return min((v for v in csp.variables if v not in assignment), key=lambda var: len(csp.domains[var]))
