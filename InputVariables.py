# This File is going to contain the input variables for the whole program, like material properties of the material
# under consideration.
#hello

Material = ['2014-T6(DF-L)', '2014-T6(DF-LT)', '2014-T6(P)', '7075-T6(P)', '7075-T6(DF-L)', '7075-T6(DF-LT)',
            '4130 Steel', '8630 Steel', '2024-T4', '356-T6 Aluminium', '2024-T3']
sigma_yield = [414, 414, 414, 503, 503, 503, 435, 550, 324, 165, 345]
shear_strength = [290, 290, 290, 331, 331,331, 345, 345, 283, 143, 283] #MPa
Density = [2800, 2800, 2800, 2810, 2810, 2810, 7850, 7850, 2780, 2670, 2780]

materials_fasteners = [
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

materials_lug = [
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