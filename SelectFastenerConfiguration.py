# This software component will select the fastener configuration according to WP4.4.
# this checks if given w allows for the number and size of fastners given constraints
import DesignClass
import random as rnd
import math
import numpy as np


debug_design = DesignClass.DesignInstance(2,2,2,22,2,2,2,2,2,100,
                                          2,2,[(3,3),(6,3)],[1,1])
#(x-coord),(z-coord)

def assign_diameter_list(design_object):
    diameter_list = [rnd.uniform(design_object.minimum_diameter, design_object.maximum_diameter) for _ in
                     range(design_object.fastener_rows)]
    return diameter_list

def calculate_centroid(design_object):
    np_D2_list = np.array(design_object.D2_list)
    np_hole_coordinate_list = np.array(design_object.hole_coordinate_list)
    holes_area = np.pi * np_D2_list ** 2 / 4
    weighted_sum_z = np.sum(np_hole_coordinate_list[: , 1]* holes_area)
    weighted_sum_x = np.sum(np_hole_coordinate_list[:, 0] * holes_area)
    centroid_x = weighted_sum_x / np.sum(holes_area)
    centroid_z = weighted_sum_z / np.sum(holes_area)

    return (centroid_x,centroid_z)


# this checks if given w allows for the number and size of fasteners
# for now only the case if the fastener diameter is constant
def fastener_spacing_check(design_object):
    np_D2_list = np.array(design_object.D2_list)
    np_hole_coordinate_list = np.array(design_object.hole_coordinate_list)

    if design_object.material == "metal":
        lower_limit = 2 * np.max(np_D2_list)
        upper_limit = 3 * np.max(np_D2_list)

    elif design_object.material == "composite":
        lower_limit = 4 * np.max(np_D2_list)
        upper_limit = 5 * np.max(np_D2_list)

    for i in range(len(design_object.diameter_properties)):
        for k in range(i + 1, len(design_object.diameter_properties)):
            distance_x = design_object.diameter_properties[i][0] - design_object.diameter_properties[k][0]
            distance_y = design_object.diameter_properties[i][1] - design_object.diameter_properties[k][1]
            r = math.sqrt(distance_x ** 2 + distance_y ** 2)
            if i != k and not lower_limit <= r <= upper_limit:
                return False

    for i in range(len(np_D2_list)):
        if not np_hole_coordinate_list[i,0] > 2 * np_D2_list[i] and design_object.length - np_hole_coordinate_list[i,0] > 2 * np_D2_list[i]:
                if not np_hole_coordinate_list[i,1] >= 2 * np_D2_list[i] and design_object.w - np_hole_coordinate_list[i,0] >= 2 * np_D2_list[i]:
                    return False

    return True


print(calculate_centroid(debug_design))


# 4.5 calculating the c.g of the fasteners the input of the function
# is a list of the different diameters from top to bottom in the vertical direction
