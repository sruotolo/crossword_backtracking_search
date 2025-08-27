import time
from collections import deque
import copy
import constants


def wordBacktrackingSearch(csp):
    result = None

    startTime = time.time()
    if ac3(csp):
        result = wordBacktrack(csp, {})
    endTime = time.time()

    return result, endTime - startTime


def wordBacktrack(csp, assignment):
    if len(assignment) == len(csp.variables):
        return assignment

    if csp.stepToSolve <= constants.MAX_STEP:
        var = selectUnassignedVariable(csp, assignment)
        for value in orderDomainValues(csp, var):
            if value is not None:
                csp.stepToSolve += 1
                print("Trying value", value, "for variable", var)
                if isConsistent(csp, var, value, assignment):
                    assignment[var] = value
                    oldDomains = copy.copy(csp.domains)
                    csp.domains[var] = [value]
                    inference = doInference(csp)
                    if inference:
                        result = wordBacktrack(csp, assignment)
                        if result:
                            return result
                    del assignment[var]
                    csp.domains = oldDomains

    return False


def doInference(csp):
    return ac3(csp)


def selectUnassignedVariable(csp, assignment):
    # choose the variable to assign according to the heuristic MRV (minimum remaining variables):
    # it chooses the variable which domain is the smallest

    return min((v for v in csp.variables if v not in assignment), key=lambda var: len(csp.domains[var]))


def orderDomainValues(csp, var):
    # use the number of conflicts to order the values according to the LCV heuristic

    return sorted(csp.domains[var], key=lambda val: countConflicts(csp, var, val))


def countConflicts(csp, var, value):
    conflicts = 0

    for otherVar in csp.constraints[var]:
        overlap = csp.variablesOverlap(var, otherVar[0])
        if overlap:
            i, j = overlap
            for otherVal in csp.domains[otherVar[0]]:
                if value[i] != otherVal[j]:
                    conflicts += 1

    return conflicts


def isConsistent(csp, var, value, assignment):
    consistent = True

    for otherVar, overlap in csp.constraints[var]:
        if otherVar in assignment:
            # if the other variable is already assigned, verify if the letters are the same and the words are different

            otherValue = assignment[otherVar]

            if value == otherValue or value[overlap[0]] != otherValue[overlap[1]]:
                consistent = False
        else:
            # if the other variable is not assigned, verify that at least a consistent word exists in the dictionary
            if not any(
                value[overlap[0]] == otherValue[overlap[1]] and value != otherValue for otherValue in csp.domains[otherVar]
            ):
                consistent = False

    for otherVar in assignment:
        otherValue = assignment[otherVar]
        if value == otherValue:
            consistent = False

    return consistent


def revise(csp, xi, xj):
    revised = False
    overlap = csp.variablesOverlap(xi, xj)

    for x in csp.domains[xi]:
        if all(x[overlap[0]] != y[overlap[1]] for y in csp.domains[xj]):
            csp.domains[xi].remove(x)
            revised = True

    return revised


def ac3(csp):
    queue = deque()
    for xi in csp.variables:
        for xj in csp.constraints[xi]:
            queue.append((xi, xj[0]))

    while queue:
        (xi, xj) = queue.popleft()
        if revise(csp, xi, xj):
            if not csp.domains[xi]:
                return False
            for xk in csp.constraints[xi]:
                if xk[0] != xj:
                    queue.append((xk[0], xi))

    return True
