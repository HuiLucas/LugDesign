# This software component will check the given input design for Pull Through Failure.
import DesignClass
import numpy as np


debug_design = DesignClass.DesignInstance(30, 5, 10, 2, 10,  w=80, material="metal", n_fast=4, \
                                            length=200, offset=20,flange_height=80, \
                                            hole_coordinate_list=[(-30, -80), (20, 80), (-20, 60), (20, -70)], D2_list=[10, 5, 9, 8], yieldstrength=83)


def check_pull_through(design_object):
    failure = True
    return failure

print(check_pull_through(debug_design))


def check_shear(Fyi,Dfo, design_object):
    Dfi = np.array(design_object.D2_list)
    shear = Fyi / (np.pi * Dfo * (design_object.t2 + design_object.t3))
    sigma_y = Fyi/(np.pi *(1/4) * (Dfo**2-Dfi**2))
    shearmax = np.sqrt((design_object.yieldstregth**2 - sigma_y**2)/3)
    if shear < shearmax:
        return True
    else:
        return False

print(check_shear(30,10,debug_design))


