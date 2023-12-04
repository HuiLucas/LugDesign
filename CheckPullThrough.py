# Please add the following: as output return True/False for whether the input design passes the pull through check, and if it does not, add an additional output
# that says one of the following: "x needs to increase", "y needs to increase", "x needs to decrease", "y needs to decrease", "Diameter needs to increase", "Diameter can decrease"
# as well as the index i that corresponds to the hole that this advice applies to. Only one advice about one hole needs to be returned
# at a time; the function can be run again to get advices for the other holes.

# This software component will check the given input design for Pull Through Failure.
import DesignClass
import numpy as np
debug_design_2 = DesignClass.DesignInstance(h=30, t1=5, t2=0.1, t3=2, D1=10, w=80, material="metal", n_fast=4, \
                                            length=10, offset=20,flange_height=80, \
                                            hole_coordinate_list=[(3, 35), (3, 65), (7, 35), (7, 65)], \
                                           D2_list=[10.5, 10.5, 10.5, 10.5], yieldstrength=83,N_lugs=2,N_Flanges=2, bottomplatewidth=100)
debug_design_1 = DesignClass.DesignInstance(h=30, t1=5, t2=0.2, t3=0.2, D1=10, w=50, material="metal", n_fast=4,
                                            length=100, offset=20, flange_height=60, bottomplatewidth=100,
                                            hole_coordinate_list=[(10, 10), (10, 90), (90, 10), (90, 90)],
                                            D2_list=[5, 5, 5, 5], yieldstrength=83,shearstrength=550,N_lugs=1,N_Flanges=2)
debug_loads = DesignClass.Load(433.6,433.6,1300.81,817.34,817.34,0)


def check_pullthrough(design_object, load_object): #checks pullout shear, if smaller than max we can decrease thickness,

    n_fast = len(design_object.D2_list)
    F_x = load_object.F_x
    F_y = load_object.F_y  # 433.60
    F_z = load_object.F_z
    M_x = load_object.M_x + F_z * 0.001 * (design_object.flange_height - design_object.w / 2)  # M_x(817.34) plus moment from F_z
    M_z = F_x * 0.001 * (design_object.flange_height - design_object.w / 2)
    Sum_A_rz2 = 0
    Sum_A_rx2 = 0
    F_yi = []
    F_y_Mx = []
    F_y_Mz = []
    F_y_load = F_y / n_fast
    # just direct load F_y:
    for i in range(len(design_object.D2_list)):
        F_yi.append(F_y_load)
    # contribution from M_x:
    for i in range(len(design_object.D2_list)):
        rz_i = design_object.hole_coordinate_list[i][1] - design_object.bottomplatewidth/2
        Sum_A_rz2 += (np.pi * 0.25 * design_object.D2_list[i] ** 2) * (rz_i ** 2)  # in mm^4
    for i in range(len(design_object.D2_list)):
        rz_i = design_object.hole_coordinate_list[i][1] - design_object.bottomplatewidth/2
        F_y_Mx.append((M_x * 1000 * rz_i * np.pi * 0.25 * design_object.D2_list[i] ** 2) / Sum_A_rz2)
    # contribution from M_z:
    for i in range(len(design_object.D2_list)):
        rx_i = design_object.hole_coordinate_list[i][0] - design_object.length/2
        Sum_A_rx2 += (np.pi * 0.25 * design_object.D2_list[i] ** 2) * (rx_i ** 2)  # in mm^4
    for i in range(len(design_object.D2_list)):
        rx_i = design_object.hole_coordinate_list[i][0] - design_object.length/2
        F_y_Mz.append((M_z * 1000 * rx_i * np.pi * 0.25 * design_object.D2_list[i] ** 2) / Sum_A_rx2)
    # adding all three components:
    for i in range(len(design_object.D2_list)):
        F_yi[i] += F_y_Mx[i] + F_y_Mz[i]

    # checking for failure:
    for i in range(len(design_object.D2_list)):
        Dfi = design_object.D2_list[i]
        Dfo = 1.8 * Dfi
        #print("Dfo",Dfo)
        shear = F_yi[i] / (np.pi * (Dfo/1000) * (design_object.t2/1000))
        shear2 = F_yi[i] / (np.pi * (Dfo / 1000) * (design_object.t3 / 1000))
        print("shears",shear2, shear)
        sigma_y = F_yi[i]/(np.pi / 4 * ((Dfo/1000)**2-(Dfi/1000)**2))
        shearmax = design_object.shearstrength*10**6 #np.sqrt((design_object.yieldstrength**2 - sigma_y**2)/3)
        print("shearmax", shearmax)

        if not abs(shear) < abs(shearmax):
            xmax = 0
            xmin = design_object.length
            for hole in design_object.hole_coordinate_list:
                if hole[0] > xmax:
                    xmax = hole[0]
                if hole[0] < xmin:
                    xmin = hole[0]
            DeltaX = xmax-xmin
            zmax = 0
            zmin = design_object.bottomplatewidth
            for hole in design_object.hole_coordinate_list:
                if hole[1] > zmax:
                    zmax = hole[1]
                if hole[1] < zmin:
                    zmin = hole[1]
            DeltaZ = zmax - zmin
            if abs(design_object.hole_coordinate_list[i][0]-0.5*design_object.length) < 0.5*design_object.h*(design_object.N_Flanges-1) * design_object.t1*design_object.N_Flanges*0.5:
                return [False, "increase x", i]
            if (F_x*design_object.flange_height/(M_x+F_z*design_object.flange_height)) < DeltaX/DeltaZ:
                # if design_object.hole_coordinate_list[i][0] < design_object.bottomplatewidth/2:
                #     if  design_object.hole_coordinate_list[i][1] - 2 * design_object.D2_list[i] > 0:
                #         return [False, "decrease x", i]
                # if design_object.hole_coordinate_list[i][1] > design_object.bottomplatewidth/2:
                return [False, "increase z", i]
            else:
                return [False, "increase x", i]
            # elif abs(F_y_Mx[i]) < abs(F_y_Mz[i]):
            #     return [False, "increase t2"]
            # else:
            #     if design_object.hole_coordinate_list[i][0] > design_object.length / 2:
            #         return [False, "increase x", i]
            #     if design_object.hole_coordinate_list[i][0] < design_object.length / 2:
            #         if (design_object.hole_coordinate_list[i][0] + design_object.D2_list[i] / 2) < design_object.length/2 - design_object.h/2:
            #             if design_object.hole_coordinate_list[i][0] - 2 * design_object.D2_list[i] > 0:
            #                 return [False, "decrease x", i]
        if not shear2 < shearmax:
            return [False, "increase t3"]
    return [True, "do nothing"]

print(check_pullthrough(debug_design_1, debug_loads))

# diameter head and shank diameter ratio is 1.8
#print(calculate_centroid(debug_design_1),check_pull_through(debug_design_1) )
print("here",check_pullthrough(debug_design_2,debug_loads))