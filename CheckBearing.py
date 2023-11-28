import DesignClass as dc
import numpy as np
debug_design_2 = dc.DesignInstance(h=30, t1=5, t2=10, t3=2, D1=10, w=80, material="metal", n_fast=4, \
                                            length=200, offset=20,flange_height=80, \
                                            hole_coordinate_list=[(20, 10), (180, 60), (160, 20), (30, 60)], \
                                            D2_list=[10, 5, 9, 8], yieldstrength=83, N_lugs=2, N_Flanges=2)
debug_design_2.minimum_diameter = 3
debug_design_2.maximum_diameter = 5
debug_design_2.fastener_rows = 2
debug_design_2.n_fast = 4
debug_design_2.l = 6
#hole_coordinate_list = [(-30, -80), (20, 80), (-20, 60), (20, -70)]
#D2_list = [10, 5, 9, 8]
Fx = 400
Fz = 1200

def calculate_centroid(design_object):
    holes_area = np.pi * np.array(design_object.D2_list) ** 2 / 4
    weighted_sum_z = np.sum(np.array(design_object.hole_coordinate_list)[:, 1] * holes_area)
    weighted_sum_x = np.sum(np.array(design_object.hole_coordinate_list)[:, 0] * holes_area)
    centroid_x = weighted_sum_x / np.sum(holes_area)
    centroid_z = weighted_sum_z / np.sum(holes_area)

    return (centroid_x,centroid_z)

centroid_x, centroid_z = calculate_centroid(debug_design_2)
def get_in_plane_loads(design_object):
    f_in_planex = Fx / len(design_object.D2_list)
    f_in_planez = Fz / len(design_object.D2_list)
    r_to_cg = np.sqrt((centroid_x - design_object.l/2)**2 + (centroid_z - design_object.w/2)**2)

    M_y = 0

    if centroid_x == design_object.l/2 and centroid_z == design_object.w/2:
        M_y = 0
    elif centroid_x == design_object.l/2 and centroid_z > design_object.w/2:
        M_y = - Fx * r_to_cg
    elif centroid_x == design_object.l/2 and centroid_z < design_object.w/2:
        M_y =  Fx * r_to_cg
    elif centroid_x > design_object.l / 2 and centroid_z == design_object.w / 2:
        M_y = - Fz * r_to_cg
    elif centroid_x < design_object.l / 2 and centroid_z == design_object.w / 2:
        M_y =  Fz * r_to_cg
    elif centroid_x < design_object.l / 2 and centroid_z < design_object.w / 2:
        theta = np.arctan(np.absolute((centroid_z - design_object.w / 2) / (centroid_x - design_object.l / 2)))
        M_y =  (Fz * np.cos(theta) + Fx * np.sin(theta)) * r_to_cg

    elif centroid_x < design_object.l / 2 and centroid_z > design_object.w / 2:
        theta = np.arctan(np.absolute((centroid_z - design_object.w / 2) / (centroid_x - design_object.l / 2)))
        M_y =  (Fz * np.cos(theta)  - Fx * np.sin(theta)) * r_to_cg

    elif centroid_x > design_object.l / 2 and centroid_z > design_object.w / 2:
        theta = np.arctan(np.absolute((centroid_z - design_object.w / 2) / (centroid_x - design_object.l / 2)))
        M_y =  - (Fz * np.cos(theta)  + Fx * np.sin(theta)) * r_to_cg

    elif centroid_x > design_object.l / 2 and centroid_z < design_object.w / 2:
        theta = np.arctan(np.absolute((centroid_z - design_object.w / 2) / (centroid_x - design_object.l / 2)))
        M_y =  (-Fz * np.cos(theta)  + Fx * np.sin(theta)) * r_to_cg

    return f_in_planex , f_in_planez, M_y

def get_F_in_plane_My(design_object):
    S = np.sum(((np.array(design_object.hole_coordinate_list)[:, 0] - centroid_x) ** 2 + (np.array(design_object.hole_coordinate_list)[:, 1] - centroid_z) ** 2) *np.pi * np.array(design_object.D2_list) ** 2 / 4)
    M_y = get_in_plane_loads(design_object)[2]

    for i in range(len(design_object.D2_list)):
        distance_x_1 = design_object.hole_coordinate_list[i][0] - centroid_x
        distance_z_1 = design_object.hole_coordinate_list[i][1] - centroid_z
        r = np.sqrt(distance_x_1 ** 2 + distance_z_1 ** 2)
        A = np.pi * design_object.D2_list[i] ** 2 / 4
        F_in_plane_My = M_y * A * r / S
        print(F_in_plane_My)



#print(get_in_plane_loads(debug_design_2))
#print(calculate_centroid(debug_design_2))
#print(get_F_in_plane_My(debug_design_2))

def check_bearing_stress(design_object):

    M_y = get_in_plane_loads(design_object)[2]
    S = np.sum(((np.array(design_object.hole_coordinate_list)[:, 0] - centroid_x) ** 2 + (np.array(design_object.hole_coordinate_list)[:, 1] - centroid_z) ** 2) * np.pi * np.array(design_object.D2_list) ** 2 / 4)
    sigma = np.empty((3), int)
    sigma0 = []
    for i in range(len(design_object.D2_list)):
        distance_x_1 = design_object.hole_coordinate_list[i][0] - centroid_x
        distance_z_1 = design_object.hole_coordinate_list[i][1] - centroid_z
        r = np.sqrt(distance_x_1 ** 2 + distance_z_1 ** 2)
        A = np.pi * design_object.D2_list[i] ** 2 / 4
        P = np.sqrt(get_in_plane_loads(design_object)[0]**2 + get_in_plane_loads(design_object)[1]**2 + (M_y * A * r / S)**2)
        sigma = P / (design_object.D2_list[i] * design_object.t2)
        sigma0.append(sigma)
    if np.max(sigma0) < design_object.yieldstrength:
        print("Bearing Stress Check Pass")

check_bearing_stress(debug_design_2)


