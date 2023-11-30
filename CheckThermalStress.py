# This software component will check the given input design for Thermal Stress Failure.

materials = [
    {'material': '2014-T6(DF-L)', 'thermal_expansion_coefficient': 23 ,'elastic module': 73.1 },
    {'material': '2014-T6(DF-LT)', 'thermal_expansion_coefficient': 23,'elastic module': 73.1},
    {'material': '2014-T6(P)', 'thermal_expansion_coefficient': 23,'elastic module': 73.1},
    {'material': '7075-T6(P)', 'thermal_expansion_coefficient': 23.4,'elastic module': 71.7},
    {'material': '7075-T6(DF-L)', 'thermal_expansion_coefficient': 23.4,'elastic module': 71.7},
    {'material': '7075-T6(DF-LT)', 'thermal_expansion_coefficient': 23.4,'elastic module': 71.7},
    {'material': '4130 Steel', 'thermal_expansion_coefficient': 11.1,'elastic module': 205},
    {'material': '8630 Steel', 'thermal_expansion_coefficient': 11.3,'elastic module': 200},
    {'material': '2024-T4', 'thermal_expansion_coefficient': 23.2,'elastic module': 73.1},
    {'material': '356-T6 Aluminium', 'thermal_expansion_coefficient': 23.8,'elastic module': 72.4},
    {'material': '2024-T3', 'thermal_expansion_coefficient': 21.6,'elastic module': 73.1}
]

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


def thermal_stress_calculation(design_object, lower_temp , ref_temp , phi_list , materials):
    temp_diff = math.abs(ref_temp - lower_temp)
    np_d2_list = np.array(design_object.D2_list)
    #np_phi_list = np.
    #thermal_force = np_d2_list ** 2 / 4 * temp_diff *

