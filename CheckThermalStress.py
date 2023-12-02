# This software component will check the given input design for Thermal Stress Failure.
import numpy as np
import InputVariables
import DesignClass

# assumption is that for the temperature the coefficient remains linear . mention limitation
# aluminum https://ntrs.nasa.gov/api/citations/19720023885/downloads/19720023885.pdf
# 7075-T6 https://www.matweb.com/search/datasheet_print.aspx?matguid=4f19a42be94546b686bbf43f79c51b7d
# 4130 steel https://industeel.arcelormittal.com/fichier/ds-mold-4130/
#8630 steel https://dl.asminternational.org/handbooks/edited-volume/9/chapter/113443/Thermal-Properties-of-Carbon-and-Low-Alloy-Steels
# 2024-T4 https://www.gabrian.com/2024-aluminum-properties/
# 356-T6 Aluminium https://metalitec.zriha.com/eng/raw-materials/a356-t6
# 2024-T3 2024-T3 https://www.gabrian.com/2024-aluminum-properties

#sources for elastic module
# aluminum 2014-T6 https://asm.matweb.com/search/SpecificMaterial.asp?bassnum=MA2014T6
# 7075-T6 https://asm.matweb.com/search/SpecificMaterial.asp?bassnum=ma7075t6
# 4130 steel https://asm.matweb.com/search/SpecificMaterial.asp?bassnum=m4130r
#8630 steel https://www.efunda.com/materials/alloys/alloy_steels/show_alloy.cfm?ID=AISI_8630&show_prop=all&Page_Title=AISI%208630
# 2024-T4 https://asm.matweb.com/search/SpecificMaterial.asp?bassnum=ma2024t4
# 356-T6 Aluminium https://www.matweb.com/search/datasheet_print.aspx?matguid=d524d6bf305c4ce99414cabd1c7ed070
# 2024-T3 https://asm.matweb.com/search/SpecificMaterial.asp?bassnum=ma2024t3

debug_design_2 = DesignClass.DesignInstance(h=30, t1=5, t2=10, t3=2, D1=10, w=40, material="metal", n_fast=4, \
                                            length=80, offset=20,flange_height=80, \
                                            hole_coordinate_list=[(20, 10), (20, 30), (60, 10), (60, 30)], \
                                           D2_list=[6, 6, 6, 6], yieldstrength=83,N_lugs=1,N_Flanges=2)

def thermal_stress_calculation(design_object, upper_temp , lower_temp, ref_temp , phi_list , material_fastener , material_plate):
    temp_diff_upper = upper_temp - ref_temp
    temp_diff_lower = ref_temp - lower_temp
    np_d2_list = np.array(design_object.D2_list)
    np_phi_list = np.array(phi_list)
    for materials in InputVariables.materials_lug:
        if materials.get("material") == material_plate:
            material_wall_coeff = materials.get('thermal_expansion_coefficient')
    for materials in InputVariables.materials_fasteners:
        if materials.get("Material") == material_fastener:
            material_fastener_stiffness = float(materials.get("Youngs Modulus (GPa)"))
            material_fastener_coeff = float(materials.get("Thermal Expansion (10^-6)/K"))
    # units of thermal coefficient should be in micro(10^-6) and elasitic modulus in mega (10^9)
    print(material_fastener_coeff , "fast"),print(material_wall_coeff , "wall")
    thermal_force_upper = (np_d2_list/1000) ** 2 / 4 * 3 * temp_diff_upper * (material_fastener_coeff - material_wall_coeff) * (1-np_phi_list) * material_fastener_stiffness * 1000
    thermal_force_lower = (np_d2_list/1000) ** 2 / 4 * 3 * temp_diff_lower * (material_fastener_coeff - material_wall_coeff) * (1-np_phi_list) * material_fastener_stiffness * 1000 * -1
    if np.min(thermal_force_lower) > 0:
        return thermal_force_lower
    else:
        return thermal_force_upper

print("this", thermal_stress_calculation(debug_design_2,150,-90,15,[0.04,0.04,0.04,0.04] ,'Aluminium 7075','2014-T6(DF-L)'))

