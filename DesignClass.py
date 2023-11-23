class DesignInstance:
    def __init__(self, h, t1, t2, t3, D1, w, material, n_fast, length, offset, flange_height, hole_coordinate_list, D2_list,yieldstress):
        self.h = h
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.D1 = D1
        #self.l = l #length of backplate
        self.w = w
        self.material = material
        self.n_fast = n_fast
        self.length = length
        self.offset = offset
        self.flange_height = flange_height
        self.hole_coordinate_list = hole_coordinate_list
        self.D2_list=D2_list
        self.yieldstress=yieldstress
class Load:
    def __init__(self, F_x, F_z):
        self.F_x = F_x
        self.F_z = F_z
