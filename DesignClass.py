class DesignInstance:
    def __init__(self, h, t1, t2, t3, D1, D2, w,l, material):
        self.h = h
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.D1 = D1
        self.D2 = D2
        self.l = l #length of backplate
        self.w = w
        self.material = material

class Load:
    def __init__(self, F_x, F_z):
        self.F_x = F_x
        self.F_z = F_z
