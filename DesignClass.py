from InputVariables import materials_fasteners
class DesignInstance:
    def __init__(self, h, t1, t2, t3, D1, w, material, n_fast, length, offset, flange_height, hole_coordinate_list, \
                 D2_list, yieldstrength, N_lugs, N_Flanges, Dist_between_lugs=0, bottomplatewidth=100, shearstrength=550):
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
        self.N_lugs = N_lugs
        self.N_Flanges = N_Flanges
        self.Dist_between_lugs = Dist_between_lugs
        self.bottomplatewidth = bottomplatewidth
        self.shearstrength = shearstrength
class Load:
    def __init__(self, F_x, F_y, F_z, M_x, M_y, M_z):
        self.F_x = F_x
        self.F_y = F_y
        self.F_z = F_z
        self.M_x = M_x
        self.M_y = M_y
        self.M_z = M_z

Launch_loads = Load(346.9,346.9,1040.7,653.9,653.9,0)

# Your main file

# Nut type can either be "Hexagonal" , "Cylindrical" and hole type can either be "Nut-Tightened" or "Threaded hole"

class FastenerType:
    def __init__(self, material_name, nut_type=None, hole_type=None):
        self.material = None
        self.youngs_modulus = None
        self.thermal_coeff = None
        self.yield_stress = None
        self.nut_type = nut_type
        self.hole_type = hole_type

        if nut_type not in ["Hexagonal", "Cylindrical"]:
            print("Nut type can either be 'Hexagonal' or 'Cylindrical'")
        else:
            self.nut_type = nut_type

        if hole_type not in ["Nut-Tightened", "Threaded hole"]:
            print("Hole type can either be 'Nut-Tightened' or 'Threaded hole'")
        else:
            self.hole_type = hole_type

        if material_name:
            self.set_material(material_name)

    def set_material(self, material_name):
        for material in materials_fasteners:
            if material["Material"] == material_name:
                self.material = material_name
                self.youngs_modulus = material["Youngs Modulus (GPa)"]
                self.thermal_coeff = material["Thermal Expansion (10^-6)/K"]
                self.yield_stress = material["Ultimate Tensile Strength (MPa)"]
                return
        print("Material is not in InputVariables/materials_fastener")

