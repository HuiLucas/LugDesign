# This software component will calculate the local loads on a parametric model of the lug based on the given global
# loads, and then choose values for the variables of the lug such that the lug can sustain these loads (see WP4.3).
# This Software Component will also decide between a 1-lug or 2-lug configuration.

import numpy as np

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
# Material List:
Material = ['2014-T6', '7075-T6', '4130 Steel', '8630 Steel', '2024-T4', 'AZ91C-T6', '356-T6 Aluminium','2024-T3']
F_yield = [414, 503, 435, 550, 324, 145, 165, 345]

#Material Functions Lists (Kt)
def calculate_kt(e,D,M):
    x= e/D
    Mat = M
    c1= 0.8534+ 0.2891*x  -0.1511*x^2 -0.0035*x^3 +0.0174*x^4 -0.0038*x^5 +0.0002*x^6
    c2= 1.5030-1.5054*x +1.7453*x^2 -0.9890*x^3 +0.2838*x^4 -0.0390*x^5 +0.0020*x^6
    c3= 0.6270+ 0.9428*x  - 0.8837*x^2 +0.3900*x^3 - 0.0928*x^4 +0.0115*x^5 -0.0005*x^6
    c4= 0.9083+ 0.3195*x  - 0.2985*x^2 +0.0912*x^3 -0.0121*x^4 +0.0006*x^5
    c5= 0.6115+ 1.4003*x  - 1.6563*x^2 +0.8517*x^3 - 0.2273*x^4 +0.0306 *x^5 -0.0016*x^6
    c6= 0.7625+ 1.1900*x  - 1.5365*x^2 +0.7699*x^3 - 0.1987*x^4 +0.0258*x^5 -0.0013*x^6
    c7= 1.0065-0.7188*x +0.6110*x^2 -0.3044*x^3 +0.0813*x^4 -0.0109*x^5 +0.0006*x^6

    if Mat==Material[0]:
        curve = c1
    elif Mat==Material[1]:
        curve = c2
    elif Mat==Material[2]:
        curve = c1
    elif Mat==Material[3]:
        curve = c1
    elif Mat==Material[4]:
        curve = c4
    elif Mat==Material[5] or Mat==Material[6]:
        curve = c7
    elif Mat==Material[7]:
        curve =
    else:
        pass

    return curve





def calculate_vol(t,e,D):
    volume = pi()*(e-D/2)^2*t
    return volume

def calculate_tension_area(t,e,D):
    A_t= t*(w-D)
    return A_t

def calculate_bearing_area(t,D):
    A_br=D*t
    return A_br

def choose_curve(Mat):
