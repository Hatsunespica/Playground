from z3 import *

#For two bit vectors
def contains(x,y):
    return (x|y) == x

WIDTH=32
s = Solver()

def getAbsValue(name):
    zeros=BitVec('zeros'+name,WIDTH)
    ones=BitVec('ones'+name,WIDTH)
    s.add(zeros & ones ==0)
    return (zeros,ones)

X=getAbsValue('X')
Y=getAbsValue('Y')

def getInstanceFromAbsValue(name,absValue):
    inst=BitVec(name,WIDTH)
    s.add(contains(inst,absValue[1]))
    s.add(contains(~inst,absValue[0]))
    return inst

instX=getInstanceFromAbsValue('insX',X)
instY=getInstanceFromAbsValue('insY',Y)

def g(absX,absY):
    return (absX[0]&absY[0],absX[1]|absY[1])

G=g(X,Y)

def soundnessCheck():
    s.add(Not(And(
        contains(instX|instY,G[1]),
        contains(~(instX|instY),G[0])
    )))
    print(s.check())

def precisionCheck():
    pass

soundnessCheck()







