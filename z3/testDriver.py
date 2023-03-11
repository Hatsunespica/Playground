from z3 import *
from checks import *

SOUNDNESS_CHECK=True
PRECISION_CHECK=False

### Concrete functions ###
def bitOr(opList):
    return opList[0]|opList[1]
### ###

### Transfer functions ###

def orImpl(opList, solver):
    return (opList[0][0] & opList[1][0], opList[0][1] | opList[1][1])

assert soundnessCheck(bitOr,orImpl) == 1
#assert precisionCheck(bitOr,orImpl) !=-1

#This is a binary operator eliminating all known information
#Sound but not precise
def allToBottom(opList):
    return (0,0)

assert soundnessCheck(bitOr,allToBottom) == 1
assert precisionCheck(bitOr,allToBottom) ==-1

#returns a constant ones(opList[0]) | ones(opList[1])
#precise but not sound
def allToConstant(opList):
    return (~(opList[0][1]|opList[1][1]),opList[0][1]|opList[1][1])
assert soundnessCheck(bitOr,allToConstant) == -1
assert precisionCheck(bitOr,allToConstant) == 1


#sound but not precise
def onlyOnes(opList):
    return (0, opList[0][1] | opList[1][1])
assert soundnessCheck(bitOr,onlyOnes) == 1
assert precisionCheck(bitOr,onlyOnes) ==-1

#sound but not precise
def onlyZeros(opList):
    return (opList[0][0] & opList[1][0], 0)
assert soundnessCheck(bitOr,onlyZeros) == 1
assert precisionCheck(bitOr,onlyZeros) ==-1

#not precise and not sound
#not sound example: 0x00 | xxxx
def proj1(opList):
    return (opList[0][0], opList[0][1])
assert soundnessCheck(bitOr,proj1) == -1
assert precisionCheck(bitOr,proj1) ==-1

#same as proj1
def proj2(opList):
    return (opList[1][0], opList[1][1])
assert soundnessCheck(bitOr,proj2) == -1
assert precisionCheck(bitOr,proj2) ==-1
### Tests ###
