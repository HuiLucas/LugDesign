# This software component will select the fastener configuration according to WP4.4.
# this checks if given w allows for the number and size of fastners given constraints
import DesignClass
import random as rnd
import math
import numpy as np


debug_design = DesignClass.DesignInstance(h=30, t1=5, t2=10, t3=2, D1=10, w=80, material="metal", n_fast=4, \
                                            length=200, offset=20,flange_height=80, \
                                            hole_coordinate_list=[(20, 10), (180, 60), (160, 20), (30, 60)], \
                                            D2_list=[10, 5, 9, 8], yieldstrength=83, N_lugs=2, N_Flanges=2)

#check wether spacing constraints detailed in 4.4 are met, inputs are list of coordinates and list of diameter sizes
def fastener_spacing_check(design_object):
    np_D2_list = np.array(design_object.D2_list)
    np_hole_coordinate_list = np.array(design_object.hole_coordinate_list)

    if design_object.material == "metal":
        lower_limit = 2 * np.max(np_D2_list)
        upper_limit = 3 * np.max(np_D2_list)

    elif design_object.material == "composite":
        lower_limit = 4 * np.max(np_D2_list)
        upper_limit = 5 * np.max(np_D2_list)
    #for loop checks wether the holes are within the margin of 2 * D2 from edges. For every hole
    for i in range(len(np_D2_list)):
        if not np_hole_coordinate_list[i,0] > 2 * np_D2_list[i] or design_object.length - np_hole_coordinate_list[i,0] > 2 * np_D2_list[i]:
            if np_hole_coordinate_list[i,0] - 2 * np_D2_list[i] <= 0:
                return False , i , np_hole_coordinate_list[i,0] - 2 * np_D2_list[i]
            elif design_object.length - np_hole_coordinate_list[i,0] - 2 * np_D2_list[i] <=0:
                return False , i , np_hole_coordinate_list[i,0]- 2 * np_D2_list[i] <= 0
        if not np_hole_coordinate_list[i,1] >= 2 * np_D2_list[i] or design_object.w - np_hole_coordinate_list[i,0] >= 2 * np_D2_list[i]:
            if np_hole_coordinate_list[i,1] - 2 * np_D2_list[i] <= 0:
                return False , i , np_hole_coordinate_list[i,1] - 2 * np_D2_list[i] <=0
            elif design_object.length - np_hole_coordinate_list[i,1] - 2 * np_D2_list[i] <=0:
                return False , i , np_hole_coordinate_list[i,1] - 2 * np_D2_list[i] <= 0
    #lower limit and upper limit are calculated based on the material and the for loop checks wether the center to
    #center constraint complies.
    for i in range(len(np_D2_list)):
        for k in range(i + 1, len(np_D2_list)):
            distance_x = np_hole_coordinate_list[i][0] - np_hole_coordinate_list[k][0]
            distance_y = np_hole_coordinate_list[i][1] - np_hole_coordinate_list[k][1]
            distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
            if i != k and not lower_limit <= distance <= upper_limit:
                return False

    return True

print(fastener_spacing_check(debug_design))
