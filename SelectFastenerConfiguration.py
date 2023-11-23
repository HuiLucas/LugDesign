# This software component will select the fastener configuration according to WP4.4.
# this checks if given w allows for the number and size of fastners given constraints
import DesignClass
import random as rnd
import math
import numpy as np


debug_design = DesignClass.DesignInstance(2,2,2,2,2,100,"metal",10,100,10,10,[(3,3),(6,3),],[1,1])

#calculate center of gravity given diamter size list and list of coordinates [((x-coord),(z-coord)]#

def calculate_centroid(design_object):
    np_D2_list = np.array(design_object.D2_list)
    np_hole_coordinate_list = np.array(design_object.hole_coordinate_list)
    holes_area = np.pi * np_D2_list ** 2 / 4
    weighted_sum_z = np.sum(np_hole_coordinate_list[: , 1]* holes_area)
    weighted_sum_x = np.sum(np_hole_coordinate_list[:, 0] * holes_area)
    centroid_x = weighted_sum_x / np.sum(holes_area)
    centroid_z = weighted_sum_z / np.sum(holes_area)

    return (centroid_x,centroid_z)


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

    for i in range(len(np_D2_list)):
        for k in range(i + 1, len(np_D2_list)):
            distance_x = np_hole_coordinate_list[i][0] - np_hole_coordinate_list[k][0]
            distance_y = np_hole_coordinate_list[i][1] - np_hole_coordinate_list[k][1]
            distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
            if i != k and not lower_limit <= distance <= upper_limit:
                return False

    for i in range(len(np_D2_list)):
        if not np_hole_coordinate_list[i,0] > 2 * np_D2_list[i] and design_object.length - np_hole_coordinate_list[i,0] > 2 * np_D2_list[i]:
                if not np_hole_coordinate_list[i,1] >= 2 * np_D2_list[i] and design_object.w - np_hole_coordinate_list[i,0] >= 2 * np_D2_list[i]:
                    return False

    return True





