# This software component will calculate the local loads on a parametric model of the lug based on the given global
# loads, and then choose values for the variables of the lug such that the lug can sustain these loads (see WP4.3).
# This Software Component will also decide between a 1-lug or 2-lug configuration.

import numpy as np
from scipy.optimize import minimize
import math
import DesignClass
import InputVariables
from numba import jit

debug_design3 = DesignClass.DesignInstance(h=30, t1=5, t2=10, t3=2, D1=10, w=80, material="metal", n_fast=4, \
                                            length=200, offset=20,flange_height=80, \
                                            hole_coordinate_list=[(20, 10), (180, 30), (160, 20), (30, 30)], \
                                           D2_list=[10, 5, 9, 8], yieldstrength=83,N_lugs=1,N_Flanges=2)

debug_loads = DesignClass.Load(433.6,433.6,1300.81,817.34,817.34,0)





# -------------------------
# Material List:
# DF= die forging
# P = plate

@jit(nopython=True)
def calculate_ci(i, x):
    if i ==1:
        return 0.8534 + 0.2891 * x - 0.1511 * x ** 2 - 0.0035 * x ** 3 + 0.0174 * x ** 4 - 0.0038 * x ** 5 + 0.0002 * x ** 6
    elif i==2:
        return 1.5030 - 1.5054 * x + 1.7453 * x ** 2 - 0.9890 * x ** 3 + 0.2838 * x ** 4 - 0.0390 * x ** 5 + 0.0020 * x ** 6
    elif i ==3:
        return 0.6270 + 0.9428 * x - 0.8837 * x ** 2 + 0.3900 * x ** 3 - 0.0928 * x ** 4 + 0.0115 * x ** 5 - 0.0005 * x ** 6
    elif i ==4:
        return 0.9083 + 0.3195 * x - 0.2985 * x ** 2 + 0.0912 * x ** 3 - 0.0121 * x ** 4 + 0.0006 * x ** 5
    elif i==5:
        return 0.6115 + 1.4003 * x - 1.6563 * x ** 2 + 0.8517 * x ** 3 - 0.2273 * x ** 4 + 0.0306 * x ** 5 - 0.0016 * x ** 6
    elif i==6:
        return 0.7625 + 1.1900 * x - 1.5365 * x ** 2 + 0.7699 * x ** 3 - 0.1987 * x ** 4 + 0.0258 * x ** 5 - 0.0013 * x ** 6
    elif i ==7:
        return 1.0065 - 0.7188 * x + 0.6110 * x ** 2 - 0.3044 * x ** 3 + 0.0813 * x ** 4 - 0.0109 * x ** 5 + 0.0006 * x ** 6
    else:
        return 0


# Material Functions Lists (Kt)

def calculate_kt(e, D, M, t, Material_In):
    W = 2 * e
    x = W / D
    Mat = M
    #c1 = 0.8534 + 0.2891 * x - 0.1511 * x ** 2 - 0.0035 * x ** 3 + 0.0174 * x ** 4 - 0.0038 * x ** 5 + 0.0002 * x ** 6
    #c2 = 1.5030 - 1.5054 * x + 1.7453 * x ** 2 - 0.9890 * x ** 3 + 0.2838 * x ** 4 - 0.0390 * x ** 5 + 0.0020 * x ** 6
    #c3 = 0.6270 + 0.9428 * x - 0.8837 * x ** 2 + 0.3900 * x ** 3 - 0.0928 * x ** 4 + 0.0115 * x ** 5 - 0.0005 * x ** 6
    #c4 = 0.9083 + 0.3195 * x - 0.2985 * x ** 2 + 0.0912 * x ** 3 - 0.0121 * x ** 4 + 0.0006 * x ** 5
    #c5 = 0.6115 + 1.4003 * x - 1.6563 * x ** 2 + 0.8517 * x ** 3 - 0.2273 * x ** 4 + 0.0306 * x ** 5 - 0.0016 * x ** 6
    #c6 = 0.7625 + 1.1900 * x - 1.5365 * x ** 2 + 0.7699 * x ** 3 - 0.1987 * x ** 4 + 0.0258 * x ** 5 - 0.0013 * x ** 6
    #c7 = 1.0065 - 0.7188 * x + 0.6110 * x ** 2 - 0.3044 * x ** 3 + 0.0813 * x ** 4 - 0.0109 * x ** 5 + 0.0006 * x ** 6

    if Mat == Material_In[0] or Mat == Material_In[4] or Mat == Material_In[6] or Mat == Material_In[7]:
        kt = calculate_ci(1,x)
    elif (Mat == Material_In[2] or Mat == Material_In[3]) and t <= 1.27:
        kt = calculate_ci(2,x)
    elif Mat == Material_In[1] or Mat == Material_In[5]:
        kt = calculate_ci(2,x)
    elif (Mat == Material_In[2] or Mat == Material_In[3]) and t >= 1.27:
        kt = calculate_ci(4,x)
    elif Mat == Material_In[8] or Mat == Material_In[10]:
        kt = calculate_ci(4,x)
    elif Mat == Material_In[9]:
        kt = calculate_ci(7,x)
    else:
        kt = 0
        pass
    return kt

@jit(nopython=True)
def calculate_kty(w, D, t):
    x = (6 / ((4 / (0.5 * (w - D) + D / (2 * 2 ** 0.5))*t) + 2 / (0.5 * (w - D))*t)) / (D * t)
    curve = -0.0074 + 1.384 * x - 0.5613 * x ** 2 + 1.46159 * x ** 3 - 2.6979 * x ** 4 + 1.912 * x ** 5 - 0.4626 * x ** 6
    return curve

@jit(nopython=True)
def calculate_vol(t, e, D):
    volume = math.pi * (e** 2 - (D / 2) ** 2) * t
    return volume

@jit(nopython=True)
def calculate_tension_area(t, e, D):
    W = 2 * e
    A_t = t * (W - D)
    return A_t

@jit(nopython=True)
def calculate_bearing_area(t, D):
    A_br = D * t
    return A_br

@jit(nopython=True)
def choose_kby(t, D, e):
    x = e / D
    if t / D > 0.4:
        kby = -1.4512 + 4.006 * x - 2.4375 * (x ** 2) + 1.04689 * (x ** 3) - 0.3279 * (x ** 4) + 0.0612 * (
                    x ** 5) - 0.0047 * (x ** 6)
    if 0.3 < t / D <= 0.4:
        kby = -1.4512 + 4.006 * x - 2.4375 * (x ** 2) + 1.04689 * (x ** 3) - 0.32799 * (x ** 4) + 0.0612 * (
                    x ** 5) - 0.0047 * (x ** 6)
    if 0.2 < t / D <= 0.3:
        kby = -1.0836 + 2.43934 * x + 0.09407 * (x ** 2) - 0.9348 * (x ** 3) + 0.45635 * (x ** 4) - 0.0908 * (
                    x ** 5) + 0.00671 * (x ** 6)
    if 0.15 < t / D <= 0.2:
        kby = -1.4092 + 3.62945 * x - 1.3188 * (x ** 2) - 0.219 * (x ** 3) + 0.27892 * (x ** 4) - 0.07 * (
                    x ** 5) + 0.00582 * (x ** 6)
    if 0.12 < t / D <= 0.15:
        kby = -1.7669 + 5.01225 * x - 3.2457 * (x ** 2) + 0.9993 * (x ** 3) - 0.119 * (x ** 4) - 0.0044 * (
                    x ** 5) + 0.00149 * (x ** 6)
    if 0.1 < t / D <= 0.12:
        kby = -3.0275 + 9.93272 * x - 10.321 * (x ** 2) + 5.8327 * (x ** 3) - 1.8303 * (x ** 4) + 0.29884 * (
                    x ** 5) - 0.0197 * (x ** 6)
    if 0.08 < t / D <= 0.1:
        kby = -2.7484 + 8.61564 * x - 8.1903 * (x ** 2) + 4.174 * (x ** 3) - 1.1742 * (x ** 4) + 0.17149 * (
                    x ** 5) - 0.0101 * (x ** 6)
    if 0.06 < t / D <= 0.08:
        kby = -2.4114 + 7.7648 * x - 7.6285 * (x ** 2) + 4.0767 * (x ** 3) - 1.2130 * (x ** 4) + 0.1882 * (
                    x ** 5) - 0.0118 * (x ** 6)
    if 0 < t / D <= 0.06:
        kby = -2.6227 + 8.91273 * x - 0.8543 * (x ** 2) + 5.8749 * (x ** 3) - 1.9336 * (x ** 4) + 0.3295 * (
                    x ** 5) - 0.0226 * (x ** 6)

    return kby

def Optimize_Lug(Material_In2,Sigma_In,Density_In,design_object, design_loads, high_accuracy):
    # to be changed
    M_S = 1.25 * 1.1 - 1
    N_lugs = design_object.N_lugs
    N_Flanges = design_object.N_Flanges
    if high_accuracy == True:
        [i_step, j_step, k_step,l_step, Material_List] = [20, 5, 20, 50, Material_In2]
    else:
        [i_step, j_step, k_step, l_step, Material_List] = [40, 10, 40, 100, Material_In2[0:1]]
    if design_object.Dist_between_lugs == 0:
        design_object.Dist_between_lugs = 0.5
        distance = design_object.Dist_between_lugs
    else:
        distance = design_object.Dist_between_lugs
    # FORCES with safety factor of 1.25
    Fx = design_loads.F_x / (N_Flanges * N_lugs)
    Fy = design_loads.F_y / (N_Flanges * N_lugs)
    Fz = design_loads.F_z / (N_Flanges * N_lugs)
    Mx = design_loads.M_x
    My = design_loads.M_y
    Mz = design_loads.M_z  # to be changed
    material_best_configuration_dictionnary = []
    design_array = []
    # Optimisation for each material and compare the options
    # intial guesses for '2014-T6(DF-L)':
    dictionnary = []
    for material in Material_List:
        for i in Material_In2:
            if i == material:
                sigma_y = Sigma_In[Material_In2.index(i)]
        for i in range(10, 500, i_step):
            e = i * 10 ** (-3)
            for j in range(1, 50, j_step):
                t = j * 10 ** (-3)
                print("Progress:",round((i/500+j/500)*100/1.062,1), "Material:", material, flush=True)
                for k in range(10, 500, k_step):
                    D = k * 10 ** (-3)
                    for l in range(10, 900, l_step):
                        h = l * 10 ** (-3)
                        initial_guess = [e, t, D, h]
                        # e=radius outer flange, t=thickness, D=diameter of the inner circle, material

                        K_t = calculate_kt(initial_guess[0], initial_guess[1], material, initial_guess[2], Material_In2)
                        K_ty = choose_kby(initial_guess[2], initial_guess[1], initial_guess[0])


                        ### ATTENTION: optimise the mass and the yield strength
                        def objective_function(variables, material=material):
                            e, t, D, h= variables
                            volume = calculate_vol(t, e, D)
                            for i in Material_In2:
                                if i == material:
                                    rho = Density_In[Material_In2.index(i)]
                            m = rho * volume
                            return m

                        def volume_constraint(variables):
                            e, t, D, h = variables
                            return calculate_vol(t, e, D)

                        def principal_constraint(variables):
                            e, t, D, h = variables
                            # K_t = calculate_kt(e,D,material,t)
                            # K_ty = choose_kby(t,D,e)
                            A_t = calculate_tension_area(t, e, D)
                            A_br = calculate_bearing_area(t, D)
                            for i in Material_In2:
                                if i == material:
                                    sigma_y = Sigma_In[Material_In2.index(i)]*1.1 #SF for material porperties
                            if N_lugs == 2:
                                force_couple_y = My/(distance*N_Flanges)
                            else:
                                force_couple_y = My/h
                            return ((Fx / (K_t * sigma_y* A_t)) ** 1.6 + ((Fz + force_couple_y)/ (K_ty * A_br * sigma_y)) ** 1.6)**(-0.625) - 1 - M_S
                        def constraint_thickness(variables):
                            e,t,D,h =variables
                            return -t + 0.05
                        def constraint_thickness_bigger_zero(variables):
                            e,t,D,h =variables
                            return t-0.0001
                        def constraint_outer_radius(variables):
                            e,t,D,h=variables
                            return -e+0.2
                        def constraint_outer_radius_bigger_zero(variables):
                            e,t,D,h =variables
                            return e-0.0001
                        def constraint_inner_diameter(variables):
                            e,t,D,h= variables
                            return  -D+0.39
                        def constraint_inner_diameter_bigger_zero(variables):
                            e,t,D,h= variables
                            return  D-0.005
                        def constraint_dimension(variables):
                            e, t, D, h = variables
                            return e-D/2 -0.005

                        def constraint_inter_flange_distance(variables):
                            e, t, D, h = variables
                            return h-0.0001

                        def constraint_inter_flange_distance_max(variables):
                            e, t, D, h = variables
                            return -h+1

                        def moment_x_constraint(variables):
                            e,t,D,h = variables
                            sigma = (Mx*e)/((t*(2*e)**3)/12)-sigma_y*1.1
                            return sigma

                        def thickness_over_diameter_lower_limit(variables):
                            e,t,D,h = variables
                            return - e/t + 10


                        constraints = [
                            {'type': 'ineq', 'fun': volume_constraint},
                            {'type': 'eq', 'fun': principal_constraint},
                            {'type': 'ineq', 'fun': constraint_thickness},
                            {'type': 'ineq', 'fun': constraint_thickness_bigger_zero},
                            {'type': 'ineq', 'fun': constraint_outer_radius},
                            {'type': 'ineq', 'fun': constraint_outer_radius_bigger_zero},
                            {'type': 'ineq', 'fun': constraint_inner_diameter},
                            {'type': 'ineq', 'fun': constraint_inner_diameter_bigger_zero},
                            {'type': 'ineq', 'fun': constraint_dimension},
                            {'type': 'ineq', 'fun': constraint_inter_flange_distance},
                            {'type': 'ineq', 'fun': constraint_inter_flange_distance_max},
                            {'type': 'ineq', 'fun': moment_x_constraint},
                            {'type': 'ineq', 'fun': thickness_over_diameter_lower_limit}
                        ]

                        # Choose an optimization method
                        method = 'SLSQP'

                        # Call the minimize function (Turning of display makes it WAY faster as printing takes a lot of memory)
                        result = minimize(objective_function, initial_guess, method=method, constraints=constraints,
                                          options={'disp': False}, tol=0.01)

                        # Print the result
                        if result.success == True and 0.01 <= result.fun <= 0.9:
                            dictionnary.append([result.x, result.fun])
                            # print("Optimization converged successfully.")
                            # print("Optimized variables:", result.x)
                            # print("Minimum value of the objective function:", result.fun)
                        else:
                            pass
                            #print("Optimization did not converge. Check the result message for more information.")
                            #print("Message:", result.message)
            # Initialize variables to store the best configuration and its mass
            best_configuration = None
            min_mass = float('inf')
            # Iterate through the configurations
            for config in dictionnary:
                dimensions, mass = config

                # Check if the current mass is smaller than the current minimum
                if mass < min_mass:
                    min_mass = mass
                    best_configuration = config



            material_best_configuration_dictionnary.append((material,best_configuration))

        #Check of the height of the flange limited by the Fy = 433:
        height_flange = 0

        Mz = Fy * height_flange * 10 **(-3)
        MMOI = ((2*best_configuration[0][0])**3 *(best_configuration[0][1]))/12
        if MMOI == 0:
            MMOI= 0.0001
        #if stress is exceeding the yield stress = fail
        distance_to_the_shaft = height_flange - best_configuration[0][0]
        sigma = (Mz * distance_to_the_shaft)/MMOI

        design_array.append(DesignClass.DesignInstance(h=1000*best_configuration[0][3], t1=1000*best_configuration[0][1], t2=10, t3=2, D1=1000*best_configuration[0][2], \
                                                           w=2*1000*best_configuration[0][0], material=material, n_fast=4, length=200, \
                                                           offset=20,flange_height=80,hole_coordinate_list=[(20, 10), (180, 30), (160, 20), (30, 30)], \
                                                           D2_list=[10, 5, 9, 8], yieldstrength=sigma_y,N_lugs=design_object.N_lugs,N_Flanges=design_object.N_Flanges, Dist_between_lugs=design_object.Dist_between_lugs*1000)) #convert meters to millimeters

    print(material_best_configuration_dictionnary)
    return design_array

