# This file will change the design based on the part checks. It will start from an initial design, then perform all
# the checks as written in the other software components, and improve the design if possible with iterations.

import CheckBearing, CheckThermalStress, CheckPullThrough, GlobalLoadsCalculator, InputVariables, \
    PostProcessorAndVisualizer, SelectFastener, TradeOffComperator, \
    DesignClass, LocalLoadCalculatorAndLugDesignerAndLugConfigurator

import SelectFastenerConfiguration

#!!!!!!!!!!!!! For CheckPullThrough: shearstrength is now set for one material, but needs to be done for other materials as well

initial_design = DesignClass.DesignInstance(h=30, t1=5, t2=0.1, t3=2, D1=10, w=80, material="metal", n_fast=4, \
                                            length=200, offset=20,flange_height=80, \
                                            hole_coordinate_list=[(20, 10), (180, 30), (160, 20), (30, 30)], \
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

# check3 = thermal check, thermal_loads = from thermal check
# checklist = [check1, check2, check3]
# while not checklist == [True, True, True]:
# check1 = checkbearing with thermal_loads, follow advice
# check2 = checkpullthrough, follow advice
# check3 = thermal check, thermal_loads = result from thermal check
# checklist =,[check1, check2,check3]

print(out1.h, out1.t1, out1.t2, out1.t3, out1.D1, out1.w, out1.length, out1.offset, out1.flange_height, out1.yieldstrength, out1.material, out1.Dist_between_lugs, out1.N_lugs)

out1.bottomplatewidth = out1.w
out2 = SelectFastenerConfiguration.Optimize_holes(out1, False) #strange behaviour

#selectfastener

#PostProcessorAndVisualizer.Visualize(initial_design)
PostProcessorAndVisualizer.Visualize2(out2)

print(out1.h, out1.t1, out1.t2, out1.t3, out1.D1, out1.w, out1.length, out1.offset, out1.flange_height, out1.yieldstrength, out1.material, out1.Dist_between_lugs, out1.N_lugs)


# trade-off stuff

