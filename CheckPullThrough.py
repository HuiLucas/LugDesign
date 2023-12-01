# Please add the following: as output return True/False for whether the input design passes the pull through check, and if it does not, add an additional output
# that says one of the following: "x needs to increase", "y needs to increase", "x needs to decrease", "y needs to decrease", "Diameter needs to increase", "Diameter can decrease"
# as well as the index i that corresponds to the hole that this advice applies to. Only one advice about one hole needs to be returned
# at a time; the function can be run again to get advices for the other holes.



# This software component will check the given input design for Pull Through Failure.
import DesignClass
import numpy as np

debug_design_1 = DesignClass.DesignInstance(h=30, t1=5, t2=10, t3=2, D1=10, w=80, material="metal", n_fast=4, \
                                            length=200, offset=20,flange_height=80, \
                                            hole_coordinate_list=[(10, 100), (80, 10), (100, 10), (30, 100)], \
                                            D2_list=[10, 6, 6, 10], yieldstrength=83,shearstrength=550,N_lugs=1,N_Flanges=2)

def calculate_centroid1(design_object): #calculates centroid of fasteners
    np_D2_list = np.array(design_object.D2_list)
    np_hole_coordinate_list = np.array(design_object.hole_coordinate_list)
    holes_area = np.pi * 0.25 * np_D2_list ** 2
    weighted_sum_z = np.sum(np_hole_coordinate_list[: , 1]* holes_area)
    weighted_sum_x = np.sum(np_hole_coordinate_list[:, 0] * holes_area)
    centroid_x = weighted_sum_x / np.sum(holes_area)
    centroid_z = weighted_sum_z / np.sum(holes_area)
    return (centroid_x,centroid_z)

def fast_pull_force(design_object):  #Calculates the total force on each fastener (counting two components, firstly the
    # direct force from the y-direction and also the extra force (either in tension or compression) due to the distance
    # between the respective fastener and the c.g. of the fasteners)

    n_fast=len(design_object.hole_coordinate_list)
    F_y = 433.60
    M_x = 100000#817.34
    Sum_A_r2 = 0
    F_yi = []
    centroid=calculate_centroid1(design_object)
    for i in range (len(design_object.hole_coordinate_list)):
        r_i=design_object.hole_coordinate_list[i][1]-centroid[1]
        Sum_A_r2+=(np.pi*0.25*design_object.D2_list[i]**2)*(r_i**2)  #in mm^4
    for i in range (len(design_object.hole_coordinate_list)):
        r_i = design_object.hole_coordinate_list[i][1] - centroid[1]
        F_yi.append((F_y/n_fast)+((M_x*1000)*r_i*np.pi*0.25*design_object.D2_list[i]**(2))/(Sum_A_r2))
    return F_yi

def check_pullthrough(design_object): #checks pullout shear, if smaller than max we can decrease thickness,
    #if bigger we have to increase it, the function returns values of the Dinner for wich shear is bigger than shearmax
    #Dfo is the outer diameter of the bolt.
    Fyi=fast_pull_force(debug_design_1)
    print(Fyi)
    for i in range(len(design_object.D2_list)):
        Dfi = design_object.D2_list[i]
        Dfo = 1.8 * Dfi
        shear = Fyi[i] / (np.pi * (Dfo/1000) * ((design_object.t2 + design_object.t3)/1000))
        sigma_y = Fyi[i]/(np.pi *(1/4) * ((Dfo/1000)**2-(Dfi/1000)**2))
        shearmax = design_object.shearstrength*10**(6) #np.sqrt((design_object.yieldstrength**2 - sigma_y**2)/3)
        if not shear < shearmax:
            return [False , "increase_thickness"]
    return [True]

print(check_pullthrough(debug_design_1))

# diameter head and shank diameter ratio is 1.8,,
#print(calculate_centroid(debug_design_1),check_pull_through(debug_design_1) )