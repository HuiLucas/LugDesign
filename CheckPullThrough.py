# This software component will check the given input design for Pull Through Failure.
import DesignClass
import numpy as np

debug_design_1 = DesignClass.DesignInstance(h=0.030, t1=0.005, t2=0.010, t3=0.002, D1=0.01, w=0.08, material="metal", n_fast=4, \
                                            length=0.200, offset=0.020,flange_height=0.08, \
                                            hole_coordinate_list=[(0.020, 0.010), (0.180, 0.060), (0.160, 0.020), (0.030, 0.060)], \
                                            D2_list=[0.010, 0.005, 0.009, 0.008], yieldstrength=83*10^9, N_lugs=2, N_Flanges=2)


def calculate_centroid(design_object): #calculates centroid of fasteners
    np_D2_list = np.array(design_object.D2_list)
    np_hole_coordinate_list = np.array(design_object.hole_coordinate_list)
    holes_area = np.pi * np_D2_list ** 2 / 4
    weighted_sum_z = np.sum(np_hole_coordinate_list[: , 1]* holes_area)
    weighted_sum_x = np.sum(np_hole_coordinate_list[:, 0] * holes_area)
    centroid_x = weighted_sum_x / np.sum(holes_area)
    centroid_z = weighted_sum_z / np.sum(holes_area)

    return (centroid_x,centroid_z)

def check_pull_through(design_object):  #Calculates the total force on each fastener (counting two components, firstly the
    # direct force from the y-direction and also the extra force (either in tension or compression) due to the distance
    # between the respective fastener and the c.g. of the fasteners)

    n_fast=len(design_object.hole_coordinate_list)
    F_y = 346.9
    M_x = 719.26
    Sum_A_r = 0
    F_yi = []
    centroid=calculate_centroid(design_object)
    for i in range (len(design_object.hole_coordinate_list)):
        D_z=design_object.hole_coordinate_list[i][1]-centroid[0]
        Sum_A_r+=(np.pi*0.25*design_object.D2_list[i]**2)*(D_z**2)
    for i in range (len(design_object.hole_coordinate_list)):
        D_z = design_object.hole_coordinate_list[i][1] - centroid[0]
        F_yi.append((F_y/n_fast)+(M_x*np.pi*0.25*design_object.D2_list[i]**(2)*D_z)/(Sum_A_r))
    return F_yi

#print(check_pull_through(debug_design_1))
Fyi=check_pull_through(debug_design_1)

def check_shear(design_object): #checks pullout shear, if smaller than max we can decrease thickness,
    #if bigger we have to increase it, the function returns values of the Dinner for wich shear is bigger than shearmax
    #Dfo is the outer diameter of the bolt.
        for i in range(len(design_object.D2_list)):
            Dfi = design_object.D2_list[i]
            Dfo = 1.8 * Dfi
            shear = Fyi[i] / (np.pi * Dfo * (design_object.t2 + design_object.t3))
            sigma_y = Fyi[i]/(np.pi *(1/4) * (Dfo**2-Dfi**2))
            shearmax = np.sqrt((design_object.yieldstrength**2 - sigma_y**2)/3)
            if not shear < shearmax:
                return False , "increse_thickness", Dfi
        return True
print(check_shear(debug_design_1))


#print(calculate_centroid(debug_design_1),check_pull_through(debug_design_1) )