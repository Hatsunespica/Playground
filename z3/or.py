from z3 import *

def concreteOp(x, y):
    return x|y

def contains(x,y):
    return (x|y) == x

WIDTH=4

### Tests ###

def orImpl(absX,absY):
    return (absX[0] & absY[0], absX[1] | absY[1])

#This is a binary operator eliminating all known information
#Sound but not precise
def allToBottom(absX,absY):
    return (0,0)

#returns a constant ones(absX) | ones(absY)
#precise but not sound
def allToConstant(absX,absY):
    return (~(absX[1]|absY[1]),absX[1]|absY[1])

#sound but not precise
def onlyOnes(absX,absY):
    return (0, absX[1] | absY[1])

#sound but not precise
def onlyZeros(absX, absY):
    return (absX[0] & absY[0], 0)

#not precise and not sound
#not sound example: 0x00 | xxxx
def proj1(absX, absY):
    return (absX[0], absX[1])

#same as proj1
def proj2(absX, absY):
    return (absY[0], absY[1])

### Tests ###

def absOp(absX, absY):
    return orImpl(absX,absY)

def getAbsValue(name, s):
    zeros=BitVec('zeros'+name,WIDTH)
    ones=BitVec('ones'+name,WIDTH)
    s.add(zeros & ones == 0)
    return (zeros,ones)

def getInstanceFromAbsValue(name,absValue,s):
    inst=BitVec(name,WIDTH)
    s.add(contains(inst,absValue[1]))
    s.add(contains(~inst,absValue[0]))
    return inst

def soundnessCheck(concreteOp,absOp):
    s=Solver()
    X = getAbsValue('X',s)
    Y = getAbsValue('Y',s)
    G=absOp(X,Y)
    instX = getInstanceFromAbsValue('insX', X,s)
    instY = getInstanceFromAbsValue('insY', Y,s)
    s.add(Not(And(
        contains(concreteOp(instX,instY),G[1]),
        contains(~concreteOp(instX,instY),G[0])
    )))
    checkRes=s.check()
    if str(checkRes)=='sat':
        print("soundness check failed!\ncounterexample:\n")
        print(s.model())
    elif str(checkRes) == 'unsat':
        print("soundness check successfully")
    else:
        print("unknown: ", checkRes)

def precisionCheck(concreteOp,absOp):
    s=Solver()
    X = getAbsValue('X',s)
    Y = getAbsValue('Y',s)
    G=absOp(X,Y)
    instG = getInstanceFromAbsValue("insG", G,s)
    instX = BitVec('insX', WIDTH)
    instY = BitVec('insY', WIDTH)
    s.add(
        ForAll([instX, instY],
               Implies(And(contains(instX, X[1]),
                           contains(~instX, X[0]),
                           contains(instY, Y[1]),
                           contains(~instY, Y[0])),
                       instG != concreteOp(instX, instY)))
    )
    checkRes=s.check()
    if str(checkRes) == 'sat':
        print("precision check failed!\ncounterexample:\n")
        print(s.model())
    elif str(checkRes) == 'unsat':
        print("precision check successfully")
    else:
        print("unknown: ",checkRes)

soundnessCheck(concreteOp,absOp)
print("=========")
precisionCheck(concreteOp,absOp)
