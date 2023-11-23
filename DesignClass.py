class DesignInstance:
    def __init__(self, h, t1, t2, t3, D1, w, material, n_fast, length, offset, flange_height, hole_coordinate_list, D2_list,yieldstrength):
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
        self.yieldstrength=yieldstrength
class Load:
    def __init__(self, F_x, F_y, F_z, M_x, M_y, M_z):
        self.F_x = F_x
        self.F_y = F_y
        self.F_z = F_z
        self.M_x = M_x
        self.M_y = M_y
        self.M_z = M_z

    Launch_loads=Load(346.9,346.9,1040.7,653.9,653.9,0)