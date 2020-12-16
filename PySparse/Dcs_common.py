
class Dcs:
    def __init__(self):
        self.nzmax = 0
        self.m = 0
        self.n = 0
        self.p = []
        self.i = []
        self.x = []
        self.nz = 0
class Dcss:
    def __init__(self):
        self.pinv = []
        self.q = []
        self.parent = []
        self.cp = []
        self.leftmost = []
        self.m2 = []
        self.lnz = []
        self.unz = []

class Dcsn:
    def __init__(self):
        self.L = None
        self.U = None
        self.pinv = []
        self.B = []

class Dcsd:
    def __init__(self):
        self.p = []
        self.q = []
        self.r = []
        self.s = []
        self.nb = 0
        self.rr = []
        self.cc = []
