from z3 import *

#For two bit vectors
def contains(x,y):
    return (x|y) == x

WIDTH=32
s = Solver()

def getAbsValue(name):
    zeros=BitVec('zeros'+name,WIDTH)
    ones=BitVec('ones'+name,WIDTH)
    s.add(zeros & ones == 0)
    return (zeros,ones)

X=getAbsValue('X')
Y=getAbsValue('Y')

def getInstanceFromAbsValue(name,absValue):
    inst=BitVec(name,WIDTH)
    s.add(contains(inst,absValue[1]))
    s.add(contains(~inst,absValue[0]))
    return inst

def g(absX,absY):
    return (absX[0]&absY[0],absX[1]|absY[1])

#This is a binary operator eliminating all known information
#Sound but not precise
allZeros=BitVec('allZeros',WIDTH)
s.add(allZeros==0)
def allToBottom(absX,absY):
    return (allZeros,allZeros)

#returns a constant ones(absX) | ones(absY)
#precise but not sound
def allToConstant(absX,absY):
    return (~(absX[1]|absY[1]),absX[1]|absY[1])

G=g(X,Y)
#G=allToBottom(X,Y)
#G=allToConstant(X,Y)

def soundnessCheck():
    instX = getInstanceFromAbsValue('insX', X)
    instY = getInstanceFromAbsValue('insY', Y)
    s.add(Not(And(
        contains(instX|instY,G[1]),
        contains(~(instX|instY),G[0])
    )))
    if str(s.check())=='sat':
        print("soundness check failed!\ncounterexample:\n")
        print(s.model())
    else:
        print("soundness check successfully")

def precisionCheck():
    instG = getInstanceFromAbsValue("insG", G)
    instX = BitVec('insX', WIDTH)
    instY = BitVec('insY', WIDTH)
    s.add(
        ForAll([instX, instY],
               Implies(And(contains(instX, X[1]),
                           contains(~instX, X[0]),
                           contains(instY, Y[1]),
                           contains(~instY, Y[0])),
                       instG != (instX | instY)))
    )
    if str(s.check()) == 'sat':
        print("precision check failed!\ncounterexample:\n")
        print(s.model())
    else:
        print("precision check successfully")

#soundnessCheck()
precisionCheck()
