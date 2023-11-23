import DesignClass as dc
import numpy as np
debug_design = dc.DesignInstance(30, 5, 10, 2, 10,12, 80,"metal",4,100,20,80, [(-20, -30), (20, 30), (-10, 30), (20, -20)])
debug_design.l=2
debug_design.minimum_diameter = 3
debug_design.maximum_diameter = 5
debug_design.fastener_rows = 2
debug_design.n_fast = 4
#hole_coordinate_list = [(2,3), (4,4), (6,6)]
#D2_list = [4, 5, 6]
debug_design.diameter_properties = np.array([[3,3,1],[6,3,1]])

trial_loads = dc.Load(100,1000)

def get_in_plane_loads(design_object):
    f_in_planex = dc.Load.F_x / len(design_object.diameter_properties)
    f_in_planez = dc.Load.F_z / len(design_object.diameter_properties)


    return f_in_planex , f_in_planez

