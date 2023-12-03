# This software component will select the fastener based on WP4.10.
import numpy as np
import DesignClass
debug_design = DesignClass.DesignInstance(h=30, t1=5, t2=2, t3=4, D1=10, w=80, material="metal", n_fast=4,length=200, offset=20, flange_height=80, hole_coordinate_list=[(20, 10), (180, 60), (160, 20), (30, 60)], D2_list=[9, 4, 6, 8], yieldstrength=83, N_lugs=1, N_Flanges=1)
import InputVariables



def get_youngs_modulus_lug(material_name):
    for material in InputVariables.materials_lug:
        if material["material"] == material_name:
            if isinstance(material["elastic module"], tuple):
                # If the Young's Modulus is given as a range, you can return the average
                return sum(material["elastic module"]) / len(material["Youngs Modulus (GPa)"])
            else:
                return material["elastic module"]
    # If the material name is not found
    return None




# debug_design.Ea = get_youngs_modulus("Aluminium 7075") * 10 ** 9
# debug_design.L_h_sub_type = "Hexagonal"
# debug_design.L_eng_sub_type = "Nut-Tightened"
# debug_design.Eb = get_youngs_modulus(selected_material_fastener) * 10 ** 9
# debug_design.En = get_youngs_modulus(selected_material_fastener) * 10 ** 9
# debug_design.L = [1, 2,2, 1]  # shank length
# debug_design.D = [10, 5, 9, 8]  # shank diamete

### Im gonna try to redo a bit of the code.
fastener_debug = DesignClass.FastenerType("Titanium (Grade 5)","Hexagonal","Nut-Tightened")

def get_fastener_dimensions(FastenerType,DesignInstance):
    np_D2list = np.array(DesignInstance.D2_list)
    if FastenerType.nut_type == "Hexagonal":
        height_head = (np_D2list * 0.5)
    elif FastenerType.nut_type == "Cylindrical":
        height_head = (np_D2list * 0.4)

    if FastenerType.hole_type == "Threaded hole":
        engaged_shank_length = (np_D2list * 0.33)
    elif FastenerType.hole_type == "Nut-Tightened":
        engaged_shank_length = (np_D2list * 0.4)
    #this could be the height of the nut or of the threaded insert thus the general name locking device height
    locking_device_height = (np_D2list * 0.4)
    return [height_head , engaged_shank_length , locking_device_height]

def calculate_delta_a(DesignInstance, plate_material , wall_material):
    Df_I = np.array(DesignInstance.D2_list)
    Df_O = 1.8 * Df_I
    thickness = [DesignInstance.t2,DesignInstance.t3]
    E = [get_youngs_modulus_lug(plate_material), get_youngs_modulus_lug(wall_material)]
    delta_a = []
    for i in range(2):
        delta_a_new = (4 * thickness[i]) / (E[i] * 10 ** 9 * np.pi * (Df_O ** 2 - Df_I ** 2))
        delta_a.append(delta_a_new)

    """delta_a_max = []
    
    for i in range(len(Df_O)):
        if delta_a[0][i] > delta_a[1][i]:
            delta_a_max.append(delta_a[0][i])
        else:
            delta_a_max.append(delta_a[1][i])"""

    return delta_a

print(calculate_delta_a(debug_design, "7075-T6(DF-LT)","7075-T6(DF-LT)"))

def calculate_deta_b(FastenerType,DesignInstance):
    np_D2_list = np.array(DesignInstance.D2_list)
    nominal_area = (1.8 * np_D2_list) ** 2 / 4 # maximal area of the fastener (bolt and head area --> assumption)
    shank_area = (np_D2_list - 1) ** 2 / 4 # minimum area of fastener
    head_height = get_fastener_dimensions(FastenerType,DesignInstance)[0]
    engaged_shank_length = get_fastener_dimensions(FastenerType, DesignInstance)[1]
    bolt_height = get_fastener_dimensions(FastenerType, DesignInstance)[2]
    shank_length = DesignInstance.t2 + DesignInstance.t3
    E_b = FastenerType.youngs_modulus * 10 ** 9
    delta_b = (1/E_b)*((head_height/nominal_area)+((shank_length + engaged_shank_length)/shank_area) + bolt_height/nominal_area)
    return delta_b


print(calculate_deta_b(fastener_debug,debug_design))


def calculate_force_ratio(FastenerType, DesignInstance , plate_material , wall_material):
    force_ratio = []
    delta_a = calculate_delta_a(DesignInstance,plate_material,wall_material)
    delta_b = calculate_deta_b(FastenerType, DesignInstance)
    for i in range(2):
        force_ratio_element = list(delta_a[i]/(delta_a[i]+delta_b))
        force_ratio.append(force_ratio_element)
    #check which compliance is limiting
    if force_ratio[0] > force_ratio[1]:
        return force_ratio[1] , "vehicle wall/fastener compliance is limiting"
    else:
        return force_ratio[0] , "back plate/fastener compliance is limiting"

    return force_ratio[0]

print(calculate_force_ratio(fastener_debug,debug_design,"7075-T6(DF-LT)","7075-T6(DF-LT)"))


""" def calculate_attached_parts_compliance(design_object):
    delta_a = []
    t = design_object.t2 + design_object.t3
    for i in range(len(design_object.D2_list)):
        delta_a_value = (4 * t/1000) / (design_object.Ea * math.pi * ((1.8*design_object.D2_list[i]/1000) ** 2 - (design_object.D2_list[i]/1000) ** 2))
        delta_a.append(delta_a_value)
    return delta_a



def calculate_fastener_compliance(L_h_sub_type, L_eng_sub_type, design_object):
    P = []

    for i in range(len(design_object.L)):
        print(design_object.D, design_object.L)
        A = math.pi * design_object.D[i]/1000 ** 2 / 4
        P_value = design_object.L[i]/1000 / A
        P.append(P_value)

    if L_h_sub_type == "Hexagonal":
        L_h_sub = [0.5*i for i in design_object.D2_list]
    elif L_h_sub_type == "Cylindrical":
        L_h_sub = [0.4*i for i in design_object.D2_list]
    if L_eng_sub_type == "Nut-Tightened":
        L_eng_sub = [0.4*i for i in design_object.D2_list]
    elif L_eng_sub_type == "Threaded hole":
        L_eng_sub = [0.33*i for i in design_object.D2_list]

    L_n_sub = [0.4*i for i in design_object.D2_list]

    delta_b = []
    for i in range(len(design_object.D2_list)):

        delta_b_value = 1 / design_object.Eb * (((L_h_sub[i]/1000) / math.pi * (1.8*design_object.D2_list[i]/1000) ** 2 / 4) + np.sum(P) + (L_eng_sub[i]/1000) / math.pi * (design_object.D[-1]/1000) ** 2 / 4) + (L_n_sub[i]/1000) / (design_object.En * math.pi * (1.8*design_object.D2_list[i]/1000) ** 2 / 4)
        delta_b.append(delta_b_value)
    return delta_b, L_eng_sub,L_n_sub,L_h_sub


def calculate_force_ratio(design_object):
    phi = []
    for i in range(len(design_object.delta_a)):
        phi_value = design_object.delta_a[i] / (design_object.delta_a[i] + design_object.delta_b[i])
        phi.append(phi_value)
    return phi

#
# debug_design.delta_a = calculate_attached_parts_compliance(debug_design)
# debug_design.delta_b = calculate_fastener_compliance(debug_design.L_h_sub_type, debug_design.L_eng_sub_type, debug_design)[0]
# debug_design.phi = calculate_force_ratio()


# print(f"Compliance of attached parts (delta_a): {debug_design.delta_a}")
# print(f"Compliance of fastener (delta_b): {debug_design.delta_b}")
# print(f"Force Ratio (phi): {debug_design.phi}")

def fastener_dimensions(design_object):
    fastener_diameter_L1= design_object.D2_list
    fastener_diameter_L2= [i * 0.8 for i in design_object.D2_list]
    fastener_diameter_L3= design_object.D2_list
    fastener_diameter_Head = [i * 1.8 for i in design_object.D2_list]




    return fastener_diameter_L1, fastener_diameter_L2, fastener_diameter_L3, fastener_diameter_Head

# print(f"fastener_diameter_shank_L1, fastener_diameter_shank_L2, fastener_diameter_shank_L3, fastener_diameter_Head: {fastener_dimensions(debug_design)}")
# print(f"L_h_sub, L_eng_sub, L_n_sub : {calculate_fastener_compliance(debug_design.L_h_sub_type, debug_design.L_eng_sub_type, debug_design)[1],calculate_fastener_compliance(debug_design.L_h_sub_type, debug_design.L_eng_sub_type, debug_design)[2],calculate_fastener_compliance(debug_design.L_h_sub_type, debug_design.L_eng_sub_type, debug_design)[2]}")

def fastener_length_check(design_object):
    if np.sum(design_object.L) > design_object.t2 + design_object.t3 - 1 and np.sum(design_object.L) < design_object.t2 + design_object.t3 + 1 and design_object.L[0] == design_object.L[-1]:
        L_shank_1_2_3 = design_object.L
    else:
        print("Error, the length of the shank does not match the thickness of the plate.")
        return "Error, the length of the shank does not match the thickness of the plate."

    return L_shank_1_2_3
#
# print(f"L_shank_1_2_3:{fastener_length_check(debug_design)}")

def print_material_info(material_name):
    for material in materials:
        if material["Material"] == material_name:
            print(f"Material: {material['Material']}")
            print(f"Young's Modulus (GPa): {material['Youngs Modulus (GPa)']}")
            print(f"Density (kg/m^3): {material['Density (kg/m^3)']}")
            print(f"Thermal Expansion (10^-6)/K: {material['Thermal Expansion (10^-6)/K']}")
            print(f"Ultimate Tensile Strength (MPa): {material['Ultimate Tensile Strength (MPa)']}")
            print(f"Elastic Limit(Mpa): {material['Elastic Limit(Mpa)']}")
            print(f"Resistance Factors: {material['Resistance Factors']}")
            return
    # If the material name is not found
    print(f"Material '{material_name}' not found.")

# print_material_info(selected_material_fastener)"""

# def select_fastener(design_object):
#     selected_material_fastener = "Titanium (Grade 5)"
#     design_object.L = [design_object.t2+design_object.t3 for i in range(len(design_object.D2_list))]
#     design_object.D = design_object.D2_list
#     design_object.Ea = get_youngs_modulus("Aluminium 7075") * 10 ** 9
#     design_object.L_h_sub_type = "Hexagon head"
#     design_object.L_eng_sub_type = "Nut-Tightened"
#     design_object.Eb = get_youngs_modulus(selected_material_fastener) * 10 ** 9
#     design_object.En = get_youngs_modulus(selected_material_fastener) * 10 ** 9
#     design_object.delta_a = calculate_attached_parts_compliance(design_object)
#     design_object.delta_b = calculate_fastener_compliance(design_object.L_h_sub_type, design_object.L_eng_sub_type, design_object)[0]
#     design_object.phi = calculate_force_ratio(design_object)
#     design_object.fastener_dimensions = fastener_dimensions(design_object)
#     design_object.L_shank = fastener_length_check(design_object)
# select_fastener(debug_design)