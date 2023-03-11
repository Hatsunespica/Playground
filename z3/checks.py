from z3 import *
from oracle import *

def OR(opList):
    return opList[0]|opList[1]

def AND(opList):
    return opList[0]&opList[1]

def XOR(opList):
    return opList[0]^opList[1]

#opList[0]: truncated integer
#opList[1]: specified new size
def TRUNC(opList):
    return opList[0]&((1<<opList[1])-1)

WIDTH=4

def orImpl(opList, solver):
    return (opList[0][0] & opList[1][0], opList[0][1] | opList[1][1])

def AndImpl(opList, solver):
    return (opList[0][0] | opList[0][0], opList[1][1] & opList[1][1])

def XorImpl(opList, solver):
    return ((opList[0][0]&opList[1][0])|(opList[0][1]&opList[1][1]),(opList[0][0]&opList[1][1])|(opList[0][1]&opList[1][0]))

#opList[0]: current integer
#opList[1]: new width
def TruncImpl(opList, solver):
    solver.add(opList[1]<(1<<WIDTH))
    return (TRUNC((opList[0][0],opList[1])),TRUNC((opList[0][1],opList[1])))

def absOp(opList, solver):
    return orImpl(opList,solver)

def soundnessCheck(concreteOp,absOp):
    s=Solver()
    opList=Oracle.getOperands(concreteOp.__name__,WIDTH,s)
    G=absOp(opList,s)
    instList=[]
    for i in range(len(opList)):
        if isAbsValue(opList[i]):
            instList.append(getInstanceFromAbsValue('inst'+str(i),WIDTH,opList[i],s))
        else:
            instList.append(opList[i])
    s.add(Not(And(
        contains(concreteOp(instList),G[1]),
        contains(~concreteOp(instList),G[0])
    )))
    checkRes=s.check()
    if str(checkRes)=='sat':
        print("soundness check failed!\ncounterexample:\n")
        print(s.model())
        return -1
    elif str(checkRes) == 'unsat':
        print("soundness check successfully")
        return 1
    else:
        print("unknown: ", checkRes)
        return 0

def precisionCheck(concreteOp,absOp):
    s=Solver()
    opList = Oracle.getOperands(concreteOp.__name__, WIDTH, s)
    G=absOp(opList,s)
    instG = getInstanceFromAbsValue("insG",WIDTH, G,s)
    instList=[]
    instConstraints=[]
    qualifier=[]
    for i in range(len(opList)):
        if isAbsValue(opList[i]):
            instList.append(BitVec("inst"+str(i),WIDTH))
            qualifier.append(instList[-1])
            instConstraints.append(contains(instList[-1],opList[i][1]))
            instConstraints.append(contains(~instList[-1],opList[i][0]))
        else:
            instList.append(opList[i])
    s.add(
        ForAll(qualifier,
               Implies(And(instConstraints),
                       instG != concreteOp(instList)))
    )
    checkRes=s.check()
    if str(checkRes) == 'sat':
        print("precision check failed!\ncounterexample:\n")
        print(s.model())
        return -1
    elif str(checkRes) == 'unsat':
        print("precision check successfully")
        return 1
    else:
        print("unknown: ",checkRes)
        return 0

#soundnessCheck(OR,orImpl)
#soundnessCheck(TRUNC,TruncImpl)
print("=========")
#precisionCheck(XOR,XorImpl)
