# This software component will select the fastener configuration according to WP4.4.
# this checks if given w allows for the number and size of fasteners given constraints
import numpy as np
import random

# this function creates a list that contains diameters that are going to be needed
def assign_fastner_diameter_column(fastener_rows,fastener_diameter_upper_bound, fastner_diameter_lower_bound):
    fastener_list = [random.uniform(fastner_diameter_lower_bound, fastener_diameter_upper_bound) for _ in range(fastener_rows)]
    return fastener_list

def fastener_spacing_check(w,D_2,n_fast,material):
    if material == "metal":
        if w > (n_fast-1)*2*D_2 + D_2 + 3*D_2:
            if w < (n_fast-1)*3*D_2 + D_2 + 3*D_2:
                return True
    if material == "composite":
        if w > (n_fast-1)*4*D_2 + D_2 + 3*D_2:
            if w < (n_fast-1)*5*D_2 + D_2 + 3*D_2:
                return True


while: