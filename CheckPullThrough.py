# This software component will check the given input design for Pull Through Failure.
import DesignClass
import numpy as np

debug_design_1 = DesignClass.DesignInstance(h=30, t1=5, t2=10, t3=2, D1=10, w=80, material="metal", n_fast=4, \
                                            length=200, offset=20,flange_height=80, \
                                            hole_coordinate_list=[(20, 10), (180, 60), (160, 20), (30, 60)], D2_list=[10, 5, 9, 8], yieldstrength=83)


def calculate_centroid(design_object):
    np_D2_list = np.array(design_object.D2_list)
    np_hole_coordinate_list = np.array(design_object.hole_coordinate_list)
    holes_area = np.pi * np_D2_list ** 2 / 4
    weighted_sum_z = np.sum(np_hole_coordinate_list[: , 1]* holes_area)
    weighted_sum_x = np.sum(np_hole_coordinate_list[:, 0] * holes_area)
    centroid_x = weighted_sum_x / np.sum(holes_area)
    centroid_z = weighted_sum_z / np.sum(holes_area)

    return (centroid_x,centroid_z)

def check_pull_through(design_object):
# design_object.hole_coordinate_list, design_object.D2_list
    n_fast=len(design_object.hole_coordinate_list)
    F_y = 346.9
    F_yi=(F_y/n_fast)
    return F_yi

print(check_pull_through(debug_design_1))


def check_shear(Fyi,Dfo, design_object): #checks pullout shear, if smaller than max we can decrease thickness,
    #if bigger we have to increase it, the function returns values of the Dinner for wich shear is bigger than shearmax
    #Dfo is the outer diameter of the bolt.
    if Dfo < max(design_object.D2_list):
        return False, "outer diameter too small"
    else:
        for i in range(len(design_object.D2_list)):
            Dfi = design_object.D2_list[i]
            shear = Fyi / (np.pi * Dfo * (design_object.t2 + design_object.t3))
            sigma_y = Fyi/(np.pi *(1/4) * (Dfo**2-Dfi**2))
            shearmax = np.sqrt((design_object.yieldstrength**2 - sigma_y**2)/3)
            if not shear < shearmax:
                return False , "increse_thickness", Dfi

    return True









print(calculate_centroid(debug_design_1),check_pull_through(debug_design_1) )