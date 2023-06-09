# This is a sample Python script.
import softwareproperties.cloudarchive
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from z3 import *
from functools import *
WIDTH=4
fib = Function("fib", IntSort(), IntSort())
f = Function("count_ones",BitVecSort(WIDTH),IntSort(),BitVecSort(WIDTH))

x = Int("x")
# sol.add(fib(0) == 1)
# sol.add(fib(1) == 1)
# sol.add(ForAll(x, Implies(And(x >= 2, x <= max_n), fib(x) == fib(x-1) + fib(x-2))))
# Simpler:
sol = Solver()

curWidth=Int("curWidth")
vec=BitVec("vec",WIDTH)
print((vec&1).size())
print((vec>>1).sort())
#sol.add(ForAll([curWidth,vec],If(And(curWidth>1,curWidth<=WIDTH),f(vec,curWidth)==f(vec>>1,curWidth-1)+(vec&1),f(vec,curWidth)==(vec&1))))
#tmp=BitVec("tmp",WIDTH)
tmp=BitVecVal(3,WIDTH)
tmp1=BitVec("tmp1",WIDTH)
#sol.add(tmp==tmp1>>1)

def getAllOnes():
    return BitVecVal((1<<WIDTH)-1,WIDTH)

def getZero():
    return BitVecVal(0,WIDTH)

def getBitsConstant(lowBits,highBits):
    highBits=WIDTH-highBits
    return LShR(((getAllOnes()>>lowBits)<<lowBits)<<highBits,highBits)

def getLowBitsConstant(lowBits):
    return getBitsConstant(0,lowBits)

def getHighBitsConstant(highBits):
    return getBitsConstant(WIDTH-highBits,WIDTH)

print("getHighBitConstant",getHighBitsConstant(3),simplify(getHighBitsConstant(3)))

def count_ones(b):
    n = b.size()
    bits = [ Extract(i, i, b) for i in range(n) ]
    bvs  = [ Concat(BitVecVal(0, n - 1), b) for b in bits ]
    nb   = reduce(lambda a, b: a + b, bvs)
    return nb

pow2 = [2**i for i in range(0,9)]

def getLeftmostBit(b : BitVec, solver):
    bits = [b>>i for i in pow2 if i<b.size()]
    bits.append(b)
    orBits = reduce(lambda  a, b: a | b, bits)
    return orBits - (orBits>>1)

def count_lzeros(b, solver):
    tmp_count_lzeros=BitVec("tmp_count_lzeros",WIDTH)
    leftmostBit=getLeftmostBit(b,solver)
    solver.add(leftmostBit==1<<tmp_count_lzeros)
    return b.size()-1-tmp_count_lzeros

tmp_count_lzeros=count_lzeros(tmp,sol)
def count_rzeros(b, solver):
    tmp_count_rzeros=BitVec("tmp_count_rzeros",WIDTH)
    solver.add(b-(b&(b-1))==1<<tmp_count_rzeros)
    return tmp_count_rzeros

tmp_count_rzeros=count_rzeros(tmp,sol)

def count_lones(b):
    pass

def count_rones(b):
    pass
#sol.add(BitVecVal(2,WIDTH)==sub(tmp))
#max_n = 31
#sol.add(ForAll(x, If(And(x >= 2, x <= max_n), fib(x) == fib(x-1) + fib(x-2), fib(x) == 1)))

# sol.add(x == fib(2))
#y = Int("y")
#z = Int("z")
#sol.add(y>0, y <= max_n, z >0, z <= max_n)

#sol.add(10946 == fib(y))
#sol.add(2178309 == fib(z))

print(sol)
res=sol.check()
if res==sat:
    mod = sol.model()
    # print("x:", mod.eval(x))
    print(mod)
    print("tmp:", mod.eval(tmp), "count_lzeros:",mod.eval(tmp_count_lzeros) ,
          "count_rzeros",mod.eval(tmp_count_rzeros))
    #sol.add(z != mod.eval(z),y != mod.eval(y))
else:
    print(res)