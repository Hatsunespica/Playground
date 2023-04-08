class KnownBits:
    zero = None
    one = None

    def __init__(self, zero, one):
        self.zero = zero
        self.one = one

    # This function is required
    def getConstraint(self):
        return [self.one & self.zero == 0]

    # This function is required
    def getInstanceConstraint(self, inst):
        return [(~inst | self.zero) == ~inst, (inst | self.one) == inst]


def AND(x, y):
    return x & y


def andImpl(x: KnownBits, y: KnownBits):
    return KnownBits(x.zero | y.zero, x.one & y.one)


def OR(x, y):
    return x | y


def orImpl(x: KnownBits, y: KnownBits):
    return KnownBits(x.zero & y.zero, x.one | y.one)


def XOR(x, y):
    return x ^ y


def xorImpl(x: KnownBits, y: KnownBits):
    return KnownBits((x.zero & y.zero) | (x.one & y.one), (x.zero & y.one) | (x.one & y.zero))


NEED_VERIFY = ((AND, andImpl), (OR, orImpl), (XOR, xorImpl))
