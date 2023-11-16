# This software component will calculate the local loads on a parametric model of the lug based on the given global
# loads, and then choose values for the variables of the lug such that the lug can sustain these loads (see WP4.3).
# This Software Component will also decide between a 1-lug or 2-lug configuration.

N_lugs=1
N_Flanges=2

# FORCES

Fx=381.57
Fy=381.57
Fz=1144.71
Mx=719,26
My=719,26
Mz=0 #to be changed

#-------------------------

t=1
w=1
D=1
e=1

At=t*(w-D)
Abr=D*t

