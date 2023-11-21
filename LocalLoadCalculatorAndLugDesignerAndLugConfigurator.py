# This software component will calculate the local loads on a parametric model of the lug based on the given global
# loads, and then choose values for the variables of the lug such that the lug can sustain these loads (see WP4.3).
# This Software Component will also decide between a 1-lug or 2-lug configuration.


N_lugs=1
N_Flanges=2

# FORCES

#Fx=381.57
Fy=381.57
Fz=1144.71
Mx=719,26
My=719,26
Mz=0 #to be changed

#-------------------------

def calculate_vol(t,e,D):
    volume = pi()*(e-D/2)^2*t
    return volume

def calculate_tension_area(t,e,D):
    A_t= t*(w-D)
    return A_t

def calculate_bearing_area(t,D):
    A_br=D*t
    return A_br

