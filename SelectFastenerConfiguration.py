# This software component will select the fastener configuration according to WP4.4.
# this checks if given w allows for the number and size of fastners given constraints
import MainOptimizer
import random as rnd
import numpy as np


def assign_diameter_list(design_object):
    diameter_list = [rnd.uniform(design_object.minimum_diameter, design_object.maximum_diameter) for _ in
                     range(design_object.fastener_rows)]
    return diameter_list


# this checks if given w allows for the number and size of fasteners
#for now only the case if the fastener diameter is constant
def fastener_spacing_check(design_object):
    if design_object.material == "metal":
        if design_object.w > (design_object.n_fast-1)*2*design_object.D2 + design_object.D2 + 3*design_object.D2:
            if design_object.w < (design_object.n_fast-1)*3*design_object.D2 + design_object.D2 + 3*design_object.D2:
                return True
    if design_object.material == "composite":
        if design_object.w > (design_object.n_fast-1)*4*design_object.D2 + design_object.D2 + 3*design_object.D2:
            if design_object.w < (design_object.n_fast-1)*5*design_object.D2 + design_object.D2 + 3*design_object.D2:
                return True
    return False


test_design = MainOptimizer.DesignInstance(5, 2, 2, 2, 2, 2, 5, "metal")
print(fastener_spacing_check(test_design))

#4.5 calculating the c.g of the fasteners the input of the function
#is a list of the different diameters from top to bottom in the vertical direction
