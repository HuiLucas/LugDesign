# This software component will select the fastener configuration according to WP4.4.
# this checks if given w allows for the number and size of fastners given constraints
import DesignClass
import random as rnd
import math
import numpy as np


debug_design = DesignClass.DesignInstance(h=30, t1=5, t2=10, t3=2, D1=10, w=80, material="metal", n_fast=4, \
                                            length=200, offset=20,flange_height=80, \
                                            hole_coordinate_list=[(-30, -80), (20, 80), (-20, 60), (20, -70)], D2_list=[10, 5, 9, 8])
debug_design.l = 2
debug_design.maximum_diameter = 5
debug_design.fastener_rows = 2
debug_design.n_fast = 4
#diameter list  = [[x-coord,z-coord,diameter],.......,nth hole]
debug_design.diameter_properties = np.array([[3,3,1],[6,3,1]])

def assign_diameter_list(design_object):
    diameter_list = [rnd.uniform(design_object.minimum_diameter, design_object.maximum_diameter) for _ in
                     range(design_object.fastener_rows)]
    return diameter_list

def calculate_centroid(design_object):
    holes_area = np.pi * design_object.diameter_properties[:,2] ** 2 / 4
    weighted_sum_z = np.sum(design_object.diameter_properties[: , 1]*holes_area)
    weighted_sum_x = np.sum(design_object.diameter_properties[:, 0] * holes_area)
    centroid_x = weighted_sum_x / np.sum(holes_area)
    centroid_z = weighted_sum_z / np.sum(holes_area)

    return (centroid_x,centroid_z)


# this checks if given w allows for the number and size of fasteners
# for now only the case if the fastener diameter is constant
def fastener_spacing_check(design_object):
    if design_object.material == "metal":
        lower_limit = 2 * np.max(design_object.diameter_properties[:,2])
        upper_limit = 3 * np.max(design_object.diameter_properties[:,2])

    elif design_object.material == "composite":
        lower_limit = 4 * np.max(design_object.diameter_properties[:, 2])
        upper_limit = 5 * np.max(design_object.diameter_properties[:, 2])

    for i in range(len(design_object.diameter_properties)):
        for k in range(i + 1, len(design_object.diameter_properties)):
            distance_x = design_object.diameter_properties[i][0] - design_object.diameter_properties[k][0]
            distance_y = design_object.diameter_properties[i][1] - design_object.diameter_properties[k][1]
            r = math.sqrt(distance_x ** 2 + distance_y ** 2)
            if i != k and not lower_limit <= r <= upper_limit:
                return False


    for i in design_object.diameter_properties:
        if not i[0] >= 2 * i[2] and design_object.l - i[0] >= 2 * i[2]:
                if not i[1] >= 2 * i[2] and design_object.w - i[1] >= 2*i[2]:
                    return False

    return True


print(fastener_spacing_check(debug_design))




# 4.5 calculating the c.g of the fasteners the input of the function
# is a list of the different diameters from top to bottom in the vertical direction
