# This software component will check the given input design for Pull Through Failure.
import DesignClass


debug_design = DesignClass.DesignInstance(h=30, t1=5, t2=10, t3=2, D1=10, w=80, material="metal", n_fast=4, \
                                            length=200, offset=20,flange_height=80, \
                                            hole_coordinate_list=[(20, 10), (180, 60), (160, 20), (30, 60)], D2_list=[10, 5, 9, 8])
def check_pull_through(design_object):
    failure = True
    return failure

print(check_pull_through(debug_design))