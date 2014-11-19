from random import randint

def get_SAT_struct(seq):
    """
    return SAT struct is list of list of pair
    [[(1, False), (2, True), (4, False)], [...], ...] is mean
    (1' + 2 + 4') * (...) * ...
    """
    numberClause = 0
    maxVar = -1
    sat_struct = []
    for clause in seq.split('*'):
        sat_struct.append([])
        cl = clause[1:-1] # clause without brackets
        for literal in cl.split('+'):
            if literal[-1] == "'":
                num = int(literal[:-1]) - 1 # numerate from 0 in memory
                sat_struct[numberClause].append([num, False])
            else:
                num = int(literal) - 1 # numerate from 0 in memory
                sat_struct[numberClause].append([num, True])
            maxVar = max(maxVar, num)
        numberClause += 1
    return sat_struct, maxVar + 1

def isGoodAssignment(x, sat):
    """
    x = [True, False, True, ...] is mean x1 == True, x2 == False, x3 == True, ...
    Check on True SAT on assigment x
    If SAT is True return (True, -1)
    else return (False, number error clause)
    """
    for i, clause in enumerate(sat):
        resClause = False
        for var in clause:
            resClause = resClause or (x[var[0]] == var[1])
            if resClause:
                break
        if not resClause:
            return (False, i)
    return (True, -1)

def generateRandomAssigment(numberVar):
    return [bool(randint(0,1)) for i in range(numberVar)]

def flipRandomVar(sat, numErrorClause, x):
    i = randint(0, len(sat[numErrorClause]) - 1)
    var = sat[numErrorClause][i][0]
    x[var] = not x[var]

def oneStep(sat, numberVar):
    for i in range(numberVar * 3):
        x = generateRandomAssigment(numberVar)
        isGood, numErrorClause = isGoodAssignment(x, sat)
        if isGood:
            print x
            return True
        else:
            flipRandomVar(sat, numErrorClause, x)
    return False

def solve_SAT_problem(seq="(1+2)*(1'+2')*(1'+2)*(1+2')"):
    """
    k = 3, 3-SAT
    p = (0.5 * (1 + 1/(k-1))) ** n = (0.75)**n
    If we accept probability error exp(-20)
    We need do 20/p operations oneStep
    """
    sat, numberVar = get_SAT_struct(seq)
    error = 20 # mean real error is exp(-error)
    t = int(error/((0.75)**numberVar))
    for i in range(t):
        if oneStep(sat, numberVar):
            return
    print "There is no good assigment"


if __name__ == '__main__':
    solve_SAT_problem()