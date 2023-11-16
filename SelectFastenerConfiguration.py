# This software component will select the fastener configuration according to WP4.4.
# this checks if given w allows for the number and size of fastners given constraints
def fastner_spacing_check(w,D_2,n_fast,material):
    if material == "metal":
        if w > (n_fast-1)*2*D_2 + D_2 + 3*D_2:
            if w < (n_fast-1)*3*D_2 + D_2 + 3*D_2:
                return True
    if material == "composite":
        if w > (n_fast-1)*4*D_2 + D_2 + 3*D_2:
            if w < (n_fast-1)*5*D_2 + D_2 + 3*D_2:
                return True
print(fastner_spacing_check(0.2,0.01,4,"metal"))