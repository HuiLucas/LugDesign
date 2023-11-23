import DesignClass as dc
import numpy as np
debug_design = dc.DesignInstance(h=30, t1=5, t2=10, t3=2, D1=10, w=80, material="metal", n_fast=4, \
                                            length=200, offset=20,flange_height=80, \
                                            hole_coordinate_list=[(20, 10), (180, 60), (160, 20), (30, 60)], D2_list=[10, 5, 9, 8])
debug_design.l=2
debug_design.minimum_diameter = 3
debug_design.maximum_diameter = 5
debug_design.fastener_rows = 2
debug_design.n_fast = 4
#hole_coordinate_list = [(-30, -80), (20, 80), (-20, 60), (20, -70)]
#D2_list = [10, 5, 9, 8]
debug_design.diameter_properties = np.array([[3,3,1],[6,3,1]])

trial_loads = dc.Load(100,1000)

def calculate_centroid(design_object):
    np_D2_list = np.array(design_object.D2_list)
    np_hole_coordinate_list = np.array(design_object.hole_coordinate_list)
    holes_area = np.pi * np_D2_list ** 2 / 4
    weighted_sum_z = np.sum(np_hole_coordinate_list[: , 1]* holes_area)
    weighted_sum_x = np.sum(np_hole_coordinate_list[:, 0] * holes_area)
    centroid_x = weighted_sum_x / np.sum(holes_area)
    centroid_z = weighted_sum_z / np.sum(holes_area)

    return (centroid_x,centroid_z)

