# This software component will check the given input design for Thermal Stress Failure.

materials = [
    {'material': '2014-T6(DF-L)', 'thermal_expansion_coefficient': 23 ,'elastic module': },
    {'material': '2014-T6(DF-LT)', 'thermal_expansion_coefficient': 23},
    {'material': '2014-T6(P)', 'thermal_expansion_coefficient': 23},
    {'material': '7075-T6(P)', 'thermal_expansion_coefficient': 23},
    {'material': '7075-T6(DF-L)', 'thermal_expansion_coefficient': 23},
    {'material': '7075-T6(DF-LT)', 'thermal_expansion_coefficient': 23},
    {'material': '4130 Steel', 'thermal_expansion_coefficient': 11.1},
    {'material': '8630 Steel', 'thermal_expansion_coefficient': 11.3},
    {'material': '2024-T4', 'thermal_expansion_coefficient': 23.2},
    {'material': '356-T6 Aluminium', 'thermal_expansion_coefficient': 23.8},
    {'material': '2024-T3', 'thermal_expansion_coefficient': 21.6}
]

# assumption is that for the temperature the coefficient remains linear . mention limitation
# aluminum https://ntrs.nasa.gov/api/citations/19720023885/downloads/19720023885.pdf
#


def thermal_stress_calculation(design_object, lower_temp , ref_temp , phi_list , materials):
    temp_diff = math.abs(ref_temp - lower_temp)
    np_d2_list = np.array(design_object.D2_list)
    np_phi_list = np.
    thermal_force = np_d2_list ** 2 / 4 * temp_diff *

# 4130 steel https://industeel.arcelormittal.com/fichier/ds-mold-4130/
#8630 steel https://dl.asminternational.org/handbooks/edited-volume/9/chapter/113443/Thermal-Properties-of-Carbon-and-Low-Alloy-Steels
# 2024-T4 https://www.gabrian.com/2024-aluminum-properties/
# 356-T6 Aluminium https://metalitec.zriha.com/eng/raw-materials/a356-t6
# 2024-T3 2024-T3 https://www.gabrian.com/2024-aluminum-properties
