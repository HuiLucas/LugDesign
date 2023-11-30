# This software component will select the fastener based on WP4.10.
import math
import numpy as np
import DesignClass

debug_design = DesignClass.DesignInstance(h=30, t1=5, t2=4, t3=2, D1=10, w=80, material="metal", n_fast=4,length=200, offset=20, flange_height=80, hole_coordinate_list=[(20, 10), (180, 60), (160, 20), (30, 60)], D2_list=[10, 5, 9, 8], yieldstrength=83, N_lugs=1, N_Flanges=1)



materials = [
    {"Material": "316 Stainless Steel", "Youngs Modulus (GPa)": 190, "Density (kg/m^3)": 8070,
     "Thermal Expansion (10^-6)/K": 18, "Ultimate Tensile Strength (MPa)": 620,
     "Elastic Limit(Mpa)": 170, "Resistance Factors": "Excellent"},

    {"Material": "18-8 SS", "Youngs Modulus (GPa)": 193, "Density (kg/m^3)": 7930,
     "Thermal Expansion (10^-6)/K": 17.8, "Ultimate Tensile Strength (MPa)":  620,
     "Elastic Limit(Mpa)":  310, "Resistance Factors": "Respectable but not for salty environments"},

    {"Material": "Carbon Steel", "Youngs Modulus (GPa)": 200, "Density (kg/m^3)": 7870,
     "Thermal Expansion (10^-6)/K": 11.5, "Ultimate Tensile Strength (MPa)": 540, "Elastic Limit(Mpa)": 415,
     "Resistance Factors": "Excellent"},

    {"Material": "Titanium (Grade 5)", "Youngs Modulus (GPa)": 113.8, "Density (kg/m^3)": 4430,
     "Thermal Expansion (10^-6)/K": 8.6, "Ultimate Tensile Strength (MPa)": 950, "Elastic Limit(Mpa)": 880,
     "Resistance Factors": "Excellent for corrosion but poor with wear"},

    {"Material": "Brass (Yellow)", "Youngs Modulus (GPa)": 76, "Density (kg/m^3)": 8740,
     "Thermal Expansion (10^-6)/K": 21, "Ultimate Tensile Strength (MPa)": 260, "Elastic Limit(Mpa)": 90,
     "Resistance Factors": "Good corrosion resistance"},

    {"Material": "Aluminium 7075", "Youngs Modulus (GPa)": 71.7, "Density (kg/m^3)": 2810,
     "Thermal Expansion (10^-6)/K": 25.2, "Ultimate Tensile Strength (MPa)": 572, "Elastic Limit(Mpa)": 503,
     "Resistance Factors": "Moderate"}
]

def get_youngs_modulus(material_name):
    for material in materials:
        if material["Material"] == material_name:
            if isinstance(material["Youngs Modulus (GPa)"], tuple):
                # If the Young's Modulus is given as a range, you can return the average
                return sum(material["Youngs Modulus (GPa)"]) / len(material["Youngs Modulus (GPa)"])
            else:
                return material["Youngs Modulus (GPa)"]
    # If the material name is not found
    return None

selected_material_fastener = "Titanium (Grade 5)"


debug_design.Ea = get_youngs_modulus("Aluminium 7075")
debug_design.L_h_sub_type = "Hexagon head"
debug_design.L_eng_sub_type = "Nut-Tightened"
debug_design.Eb = get_youngs_modulus(selected_material_fastener)
debug_design.En = get_youngs_modulus(selected_material_fastener)
debug_design.L = [1, 2,2, 1]  # shank length
debug_design.D = [10, 5, 9, 8]  # shank diameter


def calculate_attached_parts_compliance(design_object):
    delta_a = []
    t = design_object.t2 + design_object.t3
    for i in range(len(design_object.D2_list)):
        delta_a_value = (4 * t) / (design_object.Ea * math.pi * ((1.8*design_object.D2_list[i]) ** 2 - design_object.D2_list[i] ** 2))
        delta_a.append(delta_a_value)
    return delta_a



def calculate_fastener_compliance(L_h_sub_type, L_eng_sub_type, design_object):
    P = []

    for i in range(len(design_object.L)):
        A = math.pi * design_object.D[i] ** 2 / 4
        P_value = design_object.L[i] / A
        P.append(P_value)

    if L_h_sub_type == "Hexagon head":
        L_h_sub = [0.5*i for i in design_object.D2_list]
    elif L_h_sub_type == "Cylindrical head":
        L_h_sub = [0.4*i for i in design_object.D2_list]
    if L_eng_sub_type == "Nut-Tightened":
        L_eng_sub = [0.4*i for i in design_object.D2_list]
    elif L_eng_sub_type == "Threaded hole":
        L_eng_sub = [0.33*i for i in design_object.D2_list]

    L_n_sub = [0.4*i for i in design_object.D2_list]

    delta_b = []
    for i in range(len(design_object.D2_list)):

        delta_b_value = 1 / design_object.Eb * ((L_h_sub[i] / math.pi * (1.8*design_object.D2_list[i]) ** 2 / 4) + np.sum(P) + L_eng_sub[i] / math.pi * design_object.D[-1] ** 2 / 4) + L_n_sub[i] / (design_object.En * math.pi * (1.8*design_object.D2_list[i]) ** 2 / 4)
        delta_b.append(delta_b_value)
    return delta_b, L_eng_sub,L_n_sub,L_h_sub


def calculate_force_ratio():
    phi = []
    for i in range(len(delta_a)):
        phi_value = delta_a[i] / (delta_a[i] + delta_b[i])
        phi.append(phi_value)
    return phi


delta_a = calculate_attached_parts_compliance(debug_design)
delta_b = calculate_fastener_compliance(debug_design.L_h_sub_type, debug_design.L_eng_sub_type, debug_design)[0]
phi = calculate_force_ratio()


print(f"Compliance of attached parts (delta_a): {delta_a}")
print(f"Compliance of fastener (delta_b): {delta_b}")
print(f"Force Ratio (phi): {phi}")

def fastener_dimensions(design_object):
    fastener_diameter_L1= design_object.D2_list
    fastener_diameter_L2= [i * 0.8 for i in design_object.D2_list]
    fastener_diameter_L3= design_object.D2_list
    fastener_diameter_Head = [i * 1.8 for i in design_object.D2_list]




    return fastener_diameter_L1, fastener_diameter_L2, fastener_diameter_L3, fastener_diameter_Head

print(f"fastener_diameter_shank_L1, fastener_diameter_shank_L2, fastener_diameter_shank_L3, fastener_diameter_Head: {fastener_dimensions(debug_design)}")
print(f"L_h_sub, L_eng_sub, L_n_sub : {calculate_fastener_compliance(debug_design.L_h_sub_type, debug_design.L_eng_sub_type, debug_design)[1],calculate_fastener_compliance(debug_design.L_h_sub_type, debug_design.L_eng_sub_type, debug_design)[2],calculate_fastener_compliance(debug_design.L_h_sub_type, debug_design.L_eng_sub_type, debug_design)[2]}")

def fastener_length_check(design_object):
    if np.sum(design_object.L) > design_object.t2 + design_object.t3 - 1 and np.sum(design_object.L) < design_object.t2 + design_object.t3 + 1 and design_object.L[0] == design_object.L[-1]:
        L_shank_1_2_3 = design_object.L
    else: print("Error, the length of the shank does not match the thickness of the plate.")

    return L_shank_1_2_3

print(f"L_shank_1_2_3:{fastener_length_check(debug_design)}")

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

print_material_info(selected_material_fastener)