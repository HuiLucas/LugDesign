class DesignInstance:
    def __init__(self, h, t1, t2, t3, D1, D2,l, w, material, n_fast, length, offset, flange_height, list_of_hole_center_coords):
        self.h = h
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.D1 = D1
        self.D2 = D2
        self.l = l #length of backplate
        self.w = w
        self.material = material
        self.n_fast = n_fast
        self.length = length
        self.offset = offset
        self.flange_height = flange_height
        self.list_of_hole_center_coords = list_of_hole_center_coords
