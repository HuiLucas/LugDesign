# This file will change the design based on the part checks. It will start from an initial design, then perform all
# the checks as written in the other software components, and improve the design if possible with iterations.
import copy

import CheckBearing, CheckThermalStress, CheckPullThrough, GlobalLoadsCalculator, InputVariables, \
    PostProcessorAndVisualizer, SelectFastener, TradeOffComperator, \
    DesignClass, LocalLoadCalculatorAndLugDesignerAndLugConfigurator
import numpy as np
import SelectFastenerConfiguration

# !!!!!!!!!!!! TBD:
# !!!!!!!!!!!! For CheckPullThrough: shearstrength is now set for one material, but needs to be done for other materials as well
# Done !!!!!!!!!!!! optimize/calculate dist_between_lugs (is now set at the beginning, and never changed). Maybe set equal to upper limit of what fits on the satellite?
# Done !!!!!!!!!!!! Optimize (?) D2_holes. Is now set at the beginning, and does not change troughout the process. However, it was
# chosen to change the thickness t2 instead of the diameters of the holes, but maybe it is still possible to do both? I was thinking, maybe we could make a function that looks whether it is possible to reduce the size of a given hole (in
# discrete steps that correspond to  bolt diameters), given an existing design. Then this function could be applied all the way at the end
# to reduce the size of the the holes that are not limiting. Such a function would need to find out if the design with a smaller reduced hole
# would still pass the Bearing Check (incl. updated fastener design & thermal loads) and Pull Through Check, and if that is the case, then the size of that hole would actually be decreased.
# !!!!!!!!!!!! Check EVERYTHING, make sure no mistakes in calculations. Look for mistakes in the code. Confirm results by performing checks on the resulting designs by hand.
# !!!!!!!!!!!! Run with high_accuracy = True (once) to find out if there's strange behaviour
# !!!!!!!!!!!! Finish comparison between materials (WP4.13)
# Done !!!!!!!!!!!! Set constraint that h >= 0 if N_lugs == 2
# Done !!!!!!!!!!!! Provide list of Margins of Safety, as in WP4.11


# ----------------------------------------------------------------------------------------------------------------------
# Do not change:
initial_design = DesignClass.DesignInstance(h=30, t1=5, t2=0.1, t3=2, D1=10, w=80, material="metal", n_fast=4, \
                                            length=10, offset=20,flange_height=80, \
                                            hole_coordinate_list=[(3, 35), (3, 65), (7, 35), (7, 65)], \
                                           D2_list=[10.5, 10.5, 10.5, 10.5], yieldstrength=83,N_lugs=2,N_Flanges=2, bottomplatewidth=100)
# ----------------------------------------------------------------------------------------------------------------------

if initial_design.N_Flanges ==2:
    initial_design.offset = (initial_design.length - initial_design.t1 - initial_design.h)/2
else:
    initial_design.offset = (initial_design.length - initial_design.t1)/2
loads_with_SF = DesignClass.Load(433.6,433.6,1300.81,817.34,817.34,0)

fastener_array =[]
design_array2 = []
design_array = LocalLoadCalculatorAndLugDesignerAndLugConfigurator.Optimize_Lug(InputVariables.Material, \
                                                                 InputVariables.sigma_yield,InputVariables.Density,\
                                                                 initial_design, loads_with_SF, False)

for designindex in range(len(design_array)):
    out1 = copy.deepcopy(design_array[designindex])
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
    print("here2", out1.hole_coordinate_list)
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
        out1.fasteners = DesignClass.FastenerType("Titanium (Grade 5)","Hexagonal","Nut-Tightened")
        philist = SelectFastener.calculate_force_ratio(out1.fasteners, out1,out1.material,"7075-T6(DF-LT)")[0]
        thermal_loads = CheckThermalStress.thermal_stress_calculation(out1, 150, -90, 15, philist
                                                                      ,material_fastener=out1.fasteners.material,
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
        print("here", out1.hole_coordinate_list)

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



    print(out1.h, out1.t1, out1.t2, out1.t3, out1.D1, out1.w, out1.length, out1.offset, out1.flange_height, out1.yieldstrength, out1.material, out1.Dist_between_lugs, out1.N_lugs, out1.bottomplatewidth)
    print(out1.hole_coordinate_list)
    #PostProcessorAndVisualizer.Visualize2(out1)
    changez = out1.bottomplatewidth - out1.w
    out1.bottomplatewidth = out1.w
    for j in range(len(out1.hole_coordinate_list)):
        deltaZ = changez*0.5
        out1.hole_coordinate_list[j] = (out1.hole_coordinate_list[j][0], out1.hole_coordinate_list[j][1]-deltaZ)
    #PostProcessorAndVisualizer.Visualize2(out1)
    print(out1.h, out1.t1, out1.t2, out1.t3, out1.D1, out1.w, out1.length, out1.offset, out1.flange_height, out1.yieldstrength, out1.material, out1.Dist_between_lugs, out1.N_lugs, out1.bottomplatewidth)
    print("this", out1.hole_coordinate_list)

    for m in range(len(out1.D2_list)):
        SelectFastener.check_size_reduction_possibility(out1,m,loads_with_SF)

    out1 = SelectFastenerConfiguration.Optimize_holes(out1, False)

    MS_lug_Appendix_A = LocalLoadCalculatorAndLugDesignerAndLugConfigurator.M_S
    MS_lug_breaking_flange = 0
    MS_backupwallbearing = "allowable stress is unknown because different method is used"
    MS_backupwallbearinginclthermal = "allowable stress is unknown because different method is used"
    MS_backupwallpullthrough = "allowable stress is unknown because different method is used"
    MS_VehicleWallBearinginclThermal = "allowable stress is unknown because different method is used"
    MS_VehicleWallPullthrough = "allowable stress is unknown because different method is used"

    out1.MS =[]
    out1.MS.append(MS_lug_Appendix_A)
    out1.MS.append(MS_lug_breaking_flange)
    out1.MS.append(MS_backupwallbearing)
    out1.MS.append(MS_backupwallbearinginclthermal)
    out1.MS.append(MS_backupwallpullthrough)
    out1.MS.append(MS_VehicleWallBearinginclThermal)
    out1.MS.append(MS_VehicleWallPullthrough)

    #PostProcessorAndVisualizer.Visualize(initial_design)
    print(out1.hole_coordinate_list)
    #PostProcessorAndVisualizer.Visualize2(out1, designindex)

    print(out1.h, out1.t1, out1.t2, out1.t3, out1.D1, out1.w, out1.length, out1.offset, out1.flange_height, out1.yieldstrength, out1.material, out1.Dist_between_lugs, out1.N_lugs)
    out1.checklist = checklist
    print(checklist)
    design_array2.append(out1)
    print(designindex)
    print(out1.hole_coordinate_list)


for designindex in range(len(design_array2)):
    design_array2[designindex].volume = 0
    PostProcessorAndVisualizer.Visualize2(design_array2[designindex], designindex)
    # print(design_array2[designindex].material)
    # print(InputVariables.Material.index(design_array2[designindex].material))
    # print(InputVariables.Density[InputVariables.Material.index(design_array2[designindex].material)], design_array2[designindex].volume)
    # print(InputVariables.Density[InputVariables.Material.index(design_array2[designindex].material)]*design_array2[designindex].volume)
    design_array2[designindex].mass = InputVariables.Density[InputVariables.Material.index(design_array2[designindex].material)]*design_array2[designindex].volume
# trade-off stuff
TradeOffComperator.TradeOff(design_array2)