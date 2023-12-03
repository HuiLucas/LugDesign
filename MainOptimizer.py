# This file will change the design based on the part checks. It will start from an initial design, then perform all
# the checks as written in the other software components, and improve the design if possible with iterations.

import CheckBearing, CheckThermalStress, CheckPullThrough, GlobalLoadsCalculator, InputVariables, \
    PostProcessorAndVisualizer, SelectFastener, TradeOffComperator, \
    DesignClass, LocalLoadCalculatorAndLugDesignerAndLugConfigurator
import numpy as np
import SelectFastenerConfiguration

#!!!!!!!!!!!!! For CheckPullThrough: shearstrength is now set for one material, but needs to be done for other materials as well

initial_design = DesignClass.DesignInstance(h=30, t1=5, t2=0.1, t3=2, D1=10, w=80, material="metal", n_fast=4, \
                                            length=200, offset=20,flange_height=80, \
                                            hole_coordinate_list=[(70, 35), (70, 65), (130, 35), (130, 65)], \
                                           D2_list=[10, 10, 10, 10], yieldstrength=83,N_lugs=2,N_Flanges=2, bottomplatewidth=100)
if initial_design.N_Flanges ==2:
    initial_design.offset = (initial_design.length - initial_design.t1 - initial_design.h)/2
else:
    initial_design.offset = (initial_design.length - initial_design.t1)/2
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
if CheckPullThrough.check_pullthrough(out1, loads_with_SF)[0] == True:
    check2 = True
print(check2, counter2, out1.t2)
while check2 == False and counter2 < 500:
    #print(out1.hole_coordinate_list)
    print(CheckPullThrough.check_pullthrough(out1, loads_with_SF)[1])
    if CheckPullThrough.check_pullthrough(out1, loads_with_SF)[1] == "decrease z":
        for ix in range(len(out1.hole_coordinate_list)):
            out1.hole_coordinate_list[ix] = (
                out1.hole_coordinate_list[ix][0],
                0.5 * out1.bottomplatewidth + (out1.hole_coordinate_list[ix][1] - 0.5 * out1.bottomplatewidth) * 0.98)
    elif CheckPullThrough.check_pullthrough(out1, loads_with_SF)[1] == "increase z":
        for ix in range(len(out1.hole_coordinate_list)):
            out1.hole_coordinate_list[ix] = (
                out1.hole_coordinate_list[ix][0],
                0.5 * out1.bottomplatewidth + (out1.hole_coordinate_list[ix][1] - 0.5 * out1.bottomplatewidth) * 1.02)
    elif CheckPullThrough.check_pullthrough(out1, loads_with_SF)[1] == "increase x":
        for ix in range(len(out1.hole_coordinate_list)):
            out1.hole_coordinate_list[ix] = (
                0.5 * out1.length + (out1.hole_coordinate_list[ix][0] - 0.5 * out1.length) * 1.02,
                out1.hole_coordinate_list[ix][1])
    elif CheckPullThrough.check_pullthrough(out1, loads_with_SF)[1] == "decrease x":
        for ix in range(len(out1.hole_coordinate_list)):
            out1.hole_coordinate_list[ix] = (
                0.5 * out1.length + (out1.hole_coordinate_list[ix][0] - 0.5 * out1.length) * 0.98,
                out1.hole_coordinate_list[ix][1])
    elif CheckPullThrough.check_pullthrough(out1, loads_with_SF)[1] == "increase t2":
        out1.t2 += 0.1
    elif CheckPullThrough.check_pullthrough(out1, loads_with_SF)[1] == "increase t3":
        out1.t3 += 0.1
    else:
        check2 = True

    counter2 += 1
print(check2, counter2, out1.t2)




checklist = [False, False]

# checklist = [check1, check2]
counter3 = 0
while not checklist == [True, True] and counter3<100:
    fasteners = DesignClass.FastenerType("Titanium (Grade 5)","Hexagonal","Nut-Tightened")
    philist = SelectFastener.calculate_force_ratio(fasteners, out1,out1.material,"7075-T6(DF-LT)")[0]
    thermal_loads = CheckThermalStress.thermal_stress_calculation(out1, 150, -90, 15, philist
                                                                  ,material_fastener=fasteners.material,
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
    if CheckPullThrough.check_pullthrough(out1, loads_with_SF)[0] == True:
        check2 = True
    print(check2, counter2, out1.t2)
    while check2 == False and counter2 < 500:
        if CheckPullThrough.check_pullthrough(out1, loads_with_SF)[1] == "decrease z":
            for ix in range(len(out1.hole_coordinate_list)):
                out1.hole_coordinate_list[ix] = (
                out1.hole_coordinate_list[ix][0], 0.5*out1.bottomplatewidth+(out1.hole_coordinate_list[ix][1] -0.5*out1.bottomplatewidth)* 0.98)
        elif CheckPullThrough.check_pullthrough(out1, loads_with_SF)[1] == "increase z":
            for ix in range(len(out1.hole_coordinate_list)):
                out1.hole_coordinate_list[ix] = (
                out1.hole_coordinate_list[ix][0],0.5*out1.bottomplatewidth+(out1.hole_coordinate_list[ix][1] -0.5*out1.bottomplatewidth)* 1.02)
        elif CheckPullThrough.check_pullthrough(out1, loads_with_SF)[1] == "increase x":
            for ix in range(len(out1.hole_coordinate_list)):
                out1.hole_coordinate_list[ix] = (
                0.5*out1.length + (out1.hole_coordinate_list[ix][0]-0.5*out1.length) * 1.02, out1.hole_coordinate_list[ix][1])
        elif CheckPullThrough.check_pullthrough(out1, loads_with_SF)[1] == "decrease x":
            for ix in range(len(out1.hole_coordinate_list)):
                out1.hole_coordinate_list[ix] = (
                0.5*out1.length + (out1.hole_coordinate_list[ix][0]-0.5*out1.length) * 0.98, out1.hole_coordinate_list[ix][1])
        elif CheckPullThrough.check_pullthrough(out1, loads_with_SF)[1] == "increase t2":
            out1.t2 += 0.1
        elif CheckPullThrough.check_pullthrough(out1, loads_with_SF)[1] == "increase t3":
            out1.t3 += 0.1
        else:
            check2 = True

        counter2 += 1
    print(check2, counter2, out1.t2)
    checklist = [check1, check2]
    counter3 += 1



print(out1.h, out1.t1, out1.t2, out1.t3, out1.D1, out1.w, out1.length, out1.offset, out1.flange_height, out1.yieldstrength, out1.material, out1.Dist_between_lugs, out1.N_lugs)
print(out1.hole_coordinate_list)
#PostProcessorAndVisualizer.Visualize2(out1)
out1.bottomplatewidth = out1.w
out1 = SelectFastenerConfiguration.Optimize_holes(out1, False)



#PostProcessorAndVisualizer.Visualize(initial_design)
print(out1.hole_coordinate_list)
PostProcessorAndVisualizer.Visualize2(out1)

print(out1.h, out1.t1, out1.t2, out1.t3, out1.D1, out1.w, out1.length, out1.offset, out1.flange_height, out1.yieldstrength, out1.material, out1.Dist_between_lugs, out1.N_lugs)
print(checklist)

# trade-off stuff

