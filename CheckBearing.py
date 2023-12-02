# Please add the following: as output return True/False for whether the input design passes the bearingcheck, and if it does not, add an additional output
# that says one of the following: "x needs to increase", "y needs to increase", "x needs to decrease", "y needs to decrease", "Diameter needs to increase", "Diameter can decrease"
# as well as the index i that corresponds to the hole that this advice applies to. Only one advice about one hole needs to be returned
# at a time; the function can be run again to get advices for the other holes.


import DesignClass as dc
import numpy as np
debug_design_2 = dc.DesignInstance(h=30, t1=5, t2=0.1, t3=2, D1=10, w=40, material="metal", n_fast=4, \
                                            length=80, offset=20,flange_height=80, \
                                            hole_coordinate_list=[(20, 10), (20, 30), (60, 10), (60, 30)], \
                                           D2_list=[6, 6, 6, 6], yieldstrength=83,N_lugs=1,N_Flanges=2)
# debug_design_2.minimum_diameter = 3
# debug_design_2.maximum_diameter = 5
# debug_design_2.fastener_rows = 2
# debug_design_2.n_fast = 4
#debug_design_2.l = 6
#hole_coordinate_list = [(-30, -80), (20, 80), (-20, 60), (20, -70)]
#D2_list = [10, 5, 9, 8]
# Fx = 400
# Fz = 1200

debug_loads = dc.Load(433.6,433.6,1300.81,817.34,817.34,0)

def calculate_centroid(design_object):
    holes_area = np.pi * np.array(design_object.D2_list) ** 2 / 4
    weighted_sum_z = np.sum(np.array(design_object.hole_coordinate_list)[:, 1] * holes_area)
    weighted_sum_x = np.sum(np.array(design_object.hole_coordinate_list)[:, 0] * holes_area)
    centroid_x = weighted_sum_x / np.sum(holes_area)
    centroid_z = weighted_sum_z / np.sum(holes_area)

    return (centroid_x,centroid_z)

centroid_x, centroid_z = calculate_centroid(debug_design_2)
def get_in_plane_loads(design_object, load_object):
    f_in_planex = load_object.F_x / len(design_object.D2_list)
    f_in_planez = load_object.F_z / len(design_object.D2_list)
    r_to_cg = np.sqrt((centroid_x - design_object.length/2)**2 + (centroid_z - design_object.bottomplatewidth/2)**2)/1000

    M_y=0
    if centroid_x == design_object.length/2 and centroid_z == design_object.bottomplatewidth/2:
        M_y = 0
    elif centroid_x == design_object.length/2 and centroid_z > design_object.bottomplatewidth/2:
        M_y = - load_object.F_x * r_to_cg
    elif centroid_x == design_object.length/2 and centroid_z < design_object.bottomplatewidth/2:
        M_y =  load_object.F_x * r_to_cg
    elif centroid_x > design_object.length / 2 and centroid_z == design_object.bottomplatewidth / 2:
        M_y = - load_object.F_z * r_to_cg
    elif centroid_x < design_object.length / 2 and centroid_z == design_object.bottomplatewidth / 2:
        M_y =  load_object.F_z * r_to_cg
    elif centroid_x < design_object.length / 2 and centroid_z < design_object.bottomplatewidth / 2:
        theta = np.arctan(np.absolute((centroid_z - design_object.bottomplatewidth / 2) / (centroid_x - design_object.length / 2)))
        M_y =  (load_object.F_z * np.cos(theta) + load_object.F_x * np.sin(theta)) * r_to_cg

    elif centroid_x < design_object.length / 2 and centroid_z > design_object.bottomplatewidth / 2:
        theta = np.arctan(np.absolute((centroid_z - design_object.bottomplatewidth / 2) / (centroid_x - design_object.length / 2)))
        M_y =  (load_object.F_z * np.cos(theta)  - load_object.F_x * np.sin(theta)) * r_to_cg

    elif centroid_x > design_object.length / 2 and centroid_z > design_object.bottomplatewidth / 2:
        theta = np.arctan(np.absolute((centroid_z - design_object.bottomplatewidth / 2) / (centroid_x - design_object.length / 2)))
        M_y =  - (load_object.F_z * np.cos(theta)  + load_object.F_x * np.sin(theta)) * r_to_cg

    elif centroid_x > design_object.length / 2 and centroid_z < design_object.bottomplatewidth / 2:
        theta = np.arctan(np.absolute((centroid_z - design_object.bottomplatewidth / 2) / (centroid_x - design_object.length / 2)))
        M_y =  (-load_object.F_z * np.cos(theta)  + load_object.F_x * np.sin(theta)) * r_to_cg

    return f_in_planex , f_in_planez, M_y

def get_F_in_plane_My(design_object, load_object3):
    S = np.sum(((np.array(design_object.hole_coordinate_list)[:, 0] - centroid_x) ** 2 + (np.array(design_object.hole_coordinate_list)[:, 1] - centroid_z) ** 2) *np.pi * np.array(design_object.D2_list) ** 2 / 4) / (1000 ** 2)
    M_y = get_in_plane_loads(design_object, load_object3)[2]

    F_in_plane_My = []

    for i in range(len(design_object.D2_list)):
        distance_x_1 = design_object.hole_coordinate_list[i][0] - centroid_x
        distance_z_1 = design_object.hole_coordinate_list[i][1] - centroid_z
        r = np.sqrt(distance_x_1 ** 2 + distance_z_1 ** 2)/1000
        A = (np.pi * design_object.D2_list[i] ** 2 / 4)
        F_in_plane_My_value = M_y * A * r / S
        F_in_plane_My.append(F_in_plane_My_value)
    return F_in_plane_My





#print(get_in_plane_loads(debug_design_2, debug_loads))
#print(calculate_centroid(debug_design_2))
#print(get_F_in_plane_My(debug_design_2, debug_loads))

def check_bearing_stress(design_object, load_object2,thermal_force):

    M_y = get_in_plane_loads(design_object, load_object2)[2]
    S = np.sum(((np.array(design_object.hole_coordinate_list)[:, 0] - centroid_x) ** 2 + (np.array(design_object.hole_coordinate_list)[:, 1] - centroid_z) ** 2) * np.pi * np.array(design_object.D2_list) ** 2 / 4) / (1000 ** 4)

    sigma0 = []
    for i in range(len(design_object.D2_list)):
        distance_x_1 = design_object.hole_coordinate_list[i][0] - centroid_x
        distance_z_1 = design_object.hole_coordinate_list[i][1] - centroid_z
        r = np.sqrt(distance_x_1 ** 2 + distance_z_1 ** 2)/1000
        A = (np.pi * design_object.D2_list[i] ** 2 / 4)/(1000**2)
        P = np.sqrt(get_in_plane_loads(design_object, load_object2)[0]**2 + get_in_plane_loads(design_object, load_object2)[1]**2 + (M_y * A * r / S)**2 + thermal_force[i]**2)
        sigma = (P / (design_object.D2_list[i] * design_object.t2))
        sigma0.append(sigma)

    if np.max(sigma0) < design_object.yieldstrength:
        return "Bearing Stress Check Pass"
    else:
        return "Bearing Stress Check Failed, increase the thickness of the backplate "

print(check_bearing_stress(debug_design_2, debug_loads,[1533.2328,    383.3082,   1241.918568,  981.268992]))
#
# print(debug_design_2.t2)
# check1 = False
# print(check_bearing_stress(debug_design_2, debug_loads, [0, 0, 0,
#                                                                0]))
# if not check_bearing_stress(debug_design_2, debug_loads, [0, 0, 0,
#                                                                0]) == "Bearing Stress Check Failed, increase the thickness of the backplate ":
#     check1 = True
# counter1 = 0
# print(check1)
# while check1 == False and counter1 < 50:
#     debug_design_2.t2 += 0.2
#     if not check_bearing_stress(debug_design_2, debug_loads,[0,0,0,0]) == "Bearing Stress Check Failed, increase the thickness of the backplate ":
#         check1=True
#     else:
#         print("gonna increase")
#     counter1 += 1
#
# print(debug_design_2.t2, counter1)
#
#
