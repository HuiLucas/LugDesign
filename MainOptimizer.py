# This file will change the design based on the part checks. It will start from an initial design, then perform all
# the checks as written in the other software components, and improve the design if possible with iterations.

import CheckBearing, CheckThermalStress, CheckPullThrough, GlobalLoadsCalculator, InputVariables, \
    PostProcessorAndVisualizer, SelectFastener, TradeOffComperator, \
    DesignClass, LocalLoadCalculatorAndLugDesignerAndLugConfigurator

import SelectFastenerConfiguration

#!!!!!!!!!!!!! For CheckPullThrough: shearstrength is now set for one material, but needs to be done for other materials as well

initial_design = DesignClass.DesignInstance(h=30, t1=5, t2=0.1, t3=2, D1=10, w=80, material="metal", n_fast=4, \
                                            length=200, offset=20,flange_height=80, \
                                            hole_coordinate_list=[(10, 10), (10, 10), (10, 10), (10, 10)], \
                                           D2_list=[10, 5, 9, 8], yieldstrength=83,N_lugs=2,N_Flanges=2)
loads_with_SF = DesignClass.Load(433.6,433.6,1300.81,817.34,817.34,0)

# make for loop to go through every material
out1 = LocalLoadCalculatorAndLugDesignerAndLugConfigurator.Optimize_Lug(InputVariables.Material, \
                                                                 InputVariables.sigma_yield,InputVariables.Density,\
                                                                 initial_design, loads_with_SF, False)[0]
print(out1.h, out1.t1, out1.t2, out1.t3, out1.D1, out1.w, out1.length, out1.offset, out1.flange_height, out1.yieldstrength, out1.material, out1.Dist_between_lugs, out1.N_lugs)


#check1 = checkbearing without thermal loads, follow advice from result

check1 = False
if not CheckBearing.check_bearing_stress(out1, loads_with_SF, [0, 0, 0,
                                                               0]) == "Bearing Stress Check Failed, increase the thickness of the backplate ":
    check1 = True
counter1 = 0
print(check1, counter1, out1.t2)
while check1 == False and counter1 < 500:
    out1.t2 += 0.1
    if not CheckBearing.check_bearing_stress(out1, loads_with_SF,[0,0,0,0]) == "Bearing Stress Check Failed, increase the thickness of the backplate ":
        check1=True
    counter1 +=1
print(check1, counter1, out1.t2)
#check2 = checkpullthrough, follow advice from result

check2 = False
counter2 = 0
print(check2, counter2, out1.t2)
if not CheckPullThrough.check_pullthrough(out1, loads_with_SF) == [False , "increase_thickness"]:
    check2 = True
print(check2, counter2, out1.t2)
while check2 == False and counter2 < 500:
    out1.t2 += 0.1
    if not CheckPullThrough.check_pullthrough(out1, loads_with_SF) == [False , "increase_thickness"]:
        print("now")
        check2 = True
    counter2 += 1
print(check2, counter2, out1.t2)




checklist = [False, False]

# checklist = [check1, check2]
counter3 = 0
while not checklist == [True, True] and counter3<100:
    #SelectFastener.select_fastener(out1)
    thermal_loads = CheckThermalStress.thermal_stress_calculation(out1, 150, -90, 15, [0.04,0.04,0.04,0.04] #out1.phi, #!!!!! when fastener is selected use this
                                                                  ,material_fastener='Titanium (Grade 5)',
                                                                  material_plate=out1.material)[0]
    check1 = False
    if not CheckBearing.check_bearing_stress(out1, loads_with_SF, thermal_loads) == "Bearing Stress Check Failed, increase the thickness of the backplate ":
        check1 = True
    counter1 = 0
    print(check1, counter1, out1.t2)
    while check1 == False and counter1 < 500:
        out1.t2 += 0.1
        if not CheckBearing.check_bearing_stress(out1, loads_with_SF, thermal_loads) == "Bearing Stress Check Failed, increase the thickness of the backplate ":
            check1 = True
        counter1 += 1
    print(check1, counter1, out1.t2)

    # check2 = checkpullthrough, follow advice from result
    check2 = False
    counter2 = 0
    print(check2, counter2, out1.t2)
    if not CheckPullThrough.check_pullthrough(out1, loads_with_SF) == [False, "increase_thickness"]:
        check2 = True
    print(check2, counter2, out1.t2)
    while check2 == False and counter2 < 500:
        out1.t2 += 0.1
        if not CheckPullThrough.check_pullthrough(out1, loads_with_SF) == [False, "increase_thickness"]:
            print("now")
            check2 = True
        counter2 += 1
    print(check2, counter2, out1.t2)
    checklist = [check1, check2]
    counter3 += 1



print(out1.h, out1.t1, out1.t2, out1.t3, out1.D1, out1.w, out1.length, out1.offset, out1.flange_height, out1.yieldstrength, out1.material, out1.Dist_between_lugs, out1.N_lugs)

out1.bottomplatewidth = out1.w
out1 = SelectFastenerConfiguration.Optimize_holes(out1, False)



#PostProcessorAndVisualizer.Visualize(initial_design)
print(out1.hole_coordinate_list)
PostProcessorAndVisualizer.Visualize2(out1)

print(out1.h, out1.t1, out1.t2, out1.t3, out1.D1, out1.w, out1.length, out1.offset, out1.flange_height, out1.yieldstrength, out1.material, out1.Dist_between_lugs, out1.N_lugs)
print(checklist)

# trade-off stuff

