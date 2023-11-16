# This software component will select the fastener configuration according to WP4.4.
# this checks if given w allows for the number and size of fastners given constraints
import MainOptimizer
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
print(fastener_spacing_check(MainOptimizer.initial_design))