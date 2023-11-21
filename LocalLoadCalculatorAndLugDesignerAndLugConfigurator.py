# This software component will calculate the local loads on a parametric model of the lug based on the given global
# loads, and then choose values for the variables of the lug such that the lug can sustain these loads (see WP4.3).
# This Software Component will also decide between a 1-lug or 2-lug configuration.

import numpy as np
from scipy.optimize import minimize
import math

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
# Material List:
# DF= die forging
# P = plate 1
Material = ['2014-T6(DF-L)','2014-T6(DF-LT)','2014-T6(P)', '7075-T6(P)', '7075-T6(DF-L)', '7075-T6(DF-LT)', '4130 Steel', '8630 Steel', '2024-T4', '356-T6 Aluminium','2024-T3']
F_yield = [414, 414, 414, 503, 503, 503,435,550,324,165,345]
Density = [2800, 2800, 2800, 2810,2810,2810,7850,7850,2780,2670,2780]

#Material Functions Lists (Kt)
def calculate_kt(e,D,M,t):
    W = 2*e
    x= W/D
    Mat = M
    c1= 0.8534+ 0.2891*x  -0.1511*x**2 -0.0035*x**3 +0.0174*x**4 -0.0038*x**5 +0.0002*x**6
    c2= 1.5030-1.5054*x +1.7453*x**2 -0.9890*x**3 +0.2838*x**4 -0.0390*x**5 +0.0020*x**6
    c3= 0.6270+ 0.9428*x  - 0.8837*x**2 +0.3900*x**3 - 0.0928*x**4 +0.0115*x**5 -0.0005*x**6
    c4= 0.9083+ 0.3195*x  - 0.2985*x**2 +0.0912*x**3 -0.0121*x**4 +0.0006*x**5
    c5= 0.6115+ 1.4003*x  - 1.6563*x**2 +0.8517*x**3 - 0.2273*x**4 +0.0306 *x**5 -0.0016*x**6
    c6= 0.7625+ 1.1900*x  - 1.5365*x**2 +0.7699*x**3 - 0.1987*x**4 +0.0258*x**5 -0.0013*x**6
    c7= 1.0065-0.7188*x +0.6110*x**2 -0.3044*x**3 +0.0813*x**4 -0.0109*x**5 +0.0006*x**6

    if Mat==Material[0] or Mat==Material[4] or Mat==Material[6] or Mat==Material[7]:
        kt = c1
    elif (Mat==Material[2] or Mat==Material[3]) and t<=1.27:
        kt = c2
    elif Mat==Material[1] or Mat==Material[5]:
        kt = c2
    elif (Mat==Material[2] or Mat==Material[3]) and t>=1.27:
        kt = c4
    elif Mat==Material[8] or Mat==Material[10]:
        kt = c4
    elif Mat== Material[9]:
        kt = c7
    else:
        pass
    return kt

def calculate_kty(w,D,t):
    x= (6/((4/(0.5*(w-D)+D/(2*2**0.5)))+2/(0.5*(w-D))))/(D*t)
    curve= -0.0074 + 1.384*x - 0.5613*x**2 + 1.46159*x**3 - 2.6979*x**4 + 1.912*x**5 -0.4626*x**6
    return curve

def calculate_vol(t,e,D):
    volume = math.pi*(e-D/2)**2*t
    return volume

def calculate_tension_area(t,e,D):
    W = 2*e
    A_t= t*(W-D)
    return A_t

def calculate_bearing_area(t,D):
    A_br=D*t
    return A_br

def choose_kby(t,D,e ):
    x = e/D
    if t/D >= 0.6 :
        kby = -1.4512+ 4.006*x -2.4375 * (x**2 )+1.04689* (x**3) - 0.3279* (x**4) +0.0612 *(x**5) -0.0047*(x**6)
    if t/D == 0.4 :
        kby =  -1.4512+ 4.006*x - 2.4375* (x**2) +1.04689 *(x**3) - 0.32799*(x**4) +0.0612 *(x**5) -0.0047*(x**6)
    if t/D == 0.3:
        kby = -1.0836 + 2.43934 *x +0.09407* (x**2) -0.9348 *(x**3) +0.45635 *(x**4) -0.0908 *(x**5) +0.00671 *(x**6)
    if t/D == 0.2 :
        kby = -1.4092+ 3.62945*x  - 1.3188 * (x**2) -0.219 *(x**3) +0.27892 *(x**4) -0.07 *(x**5) +0.00582 *(x**6)
    if t/D == 0.15:
        kby = -1.7669+ 5.01225*x  - 3.2457 * (x**2) + 0.9993 *(x**3) - 0.119 *(x**4) -0.0044 *(x**5) +0.00149 *(x**6)
    if t/D == 0.12:
        kby = -3.0275 + 9.93272*x  - 10.321* (x**2) + 5.8327*(x**3) - 1.8303 *(x**4) + 0.29884 *(x**5) -0.0197*(x**6)
    if t/D == 0.1:
        kby= -2.7484+ 8.61564*x  - 8.1903* (x**2) + 4.174*(x**3) - 1.1742 *(x**4) + 0.17149 *(x**5) -0.0101*(x**6)
    if t/D == 0.08:
        kby= -2.4114 + 7.7648*x - 7.6285* (x**2) + 4.0767 *(x**3) - 1.2130 *(x**4) + 0.1882*(x**5) -0.0118*(x**6)
    if t/D == 0.06 :
        kby = -2.6227 + 8.91273*x - 0.8543* (x**2) + 5.8749 *(x**3)- 1.9336 *(x**4) + 0.3295 *(x**5) -0.0226*(x**6)

    return kby




#Optimisation for each material and compare the options
#intial guesses for '2014-T6(DF-L)':
initial_guess = [0.01, 0.005, 0.009]
material = '2014-T6(DF-L)'
#e=radius outer flange, t=thickness, D=diameter of the inner circle, material

### ATTENTION: optimise the density and the yield strength
def objective_function(variables, material = material):
    e, t, D = variables
    volume = calculate_vol(t,e,D)
    for i in Material:
        if i == material:
            rho = Density[Material.index(i)]
            break
    m = rho * volume
    return m
def volume_constraint(variables):
    e, t, D = variables
    return calculate_vol(t,e,D)

def principal_constraint(variables, material = material):
    e, t, D = variables
    #K_t = calculate_kt(e,D,material,t)
    #K_ty = choose_kby(t,D,e)
    A_t = calculate_tension_area(t,e,D)
    A_br = calculate_bearing_area(t,D)
    for i in Material:
        if i == material:
            Fy = F_yield[Material.index(i)]
            break
    return (Fy/(calculate_kt(e,D,material,t) * Fy * A_t))**1.6 + (Fz/(choose_kby(t,D,e) * A_br * Fy))**1.6 - 1

constraints = [
    {'type': 'ineq', 'fun': volume_constraint},
    {'type': 'eq', 'fun': principal_constraint}
]

# Choose an optimization method
method = 'SLSQP'

# Call the minimize function
result = minimize(objective_function, initial_guess, args=(material), method=method, constraints=constraints)

# Print the result
print("Optimized variables:", result.x)
print("Minimum value of the objective function:", result.fun)