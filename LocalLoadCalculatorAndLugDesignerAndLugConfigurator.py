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
# DF= die forging
# P = plate 1
Material = ['2014-T6(DF)', '7075-T6', '4130 Steel', '8630 Steel', '2024-T4', 'AZ91C-T6', '356-T6 Aluminium','2024-T3','2014-T6(P)']
F_yield = [414, 503, 435, 550, 324, 145, 165, 345, 414]

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


def choose_kby(t,D,e ):
    x = e/D
    if t/D >= 0.6 :
        kby = -1.4512+ 4.006*x -2.4375 * (x**2 )+1.04689* (x**3) - 0.3279* (x**4) +0.0612 *(x**5) -0.0047*(x**6)
    if t/D == 0.4 :
        kby =  -1.4512+ 4.006*x - 2.4375* (x**2) +1.04689 *(x**3) - 0.3279 9*(x**4) +0.0612 *(x**5) -0.0047*(x**6)
    if t/D == 0.3:
        kby = -1.0836 + 2.43934 *x +0.09407* (x**2) -0.9348 *(x**3) +0.45635 *(x**4) -0.0908 *(x**5) +0.00671 *(x**6)
    if t/D == 0.2 :
        kby = -1.4092+ 3.62945*x  - 1.3188 * (x**2) -0.219 *(x**3) +0.27892 *(x**4) -0.07 *(x**5) +0.00582 *(x**6)
    if t/D == 0.15:
        kby = -1.7669+ 5.01225*x  - 3.2457 * (x**2) + 0.9993 *(x**3) - 0.119 *(x**4) -0.0044 *(x**5) +0.00149 *(x**6)
    if t/D == 0.12
        kby = -3.0275 + 9.93272*x  - 10.321* (x**2) + 5.8327*(x**3) - 1.8303 *(x**4) + 0.29884 *(x**5) -0.0197*(x**6)
    if t/D == 0.1:
        kby= -2.7484+ 8.61564*x  - 8.1903* (x**2) + 4.174*(x**3) - 1.1742 *(x**4) + 0.17149 *(x**5) -0.0101*(x**6)
    if t/D == 0.08:
        kby= -2.4114 + 7.7648*x - 7.6285* (x**2) + 4.0767 *(x**3) - 1.2130 *(x**4) + 0.1882*(x**5) -0.0118*(x**6)
    if t/D == 0.06 :
        kby = -2.6227 + 8.91273*x - 0.8543* (x**2) + 5.8749 *(x**3)- 1.9336 *(x**4) + 0.3295 *(x**5) -0.0226*(x**6)

    return kby
