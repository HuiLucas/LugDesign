# This file will change the design based on the part checks. It will start from an initial design, then perform all
# the checks as written in the other software components, and improve the design if possible with iterations.

import CheckBearing, CheckThermalStress, CheckPullThrough, GlobalLoadsCalculator, InputVariables, \
    PostProcessorAndVisualizer, SelectFastener, TradeOffComperator, \
    DesignClass, LocalLoadCalculatorAndLugDesignerAndLugConfigurator

import SelectFastenerConfiguration



initial_design = DesignClass.DesignInstance(h=30, t1=5, t2=10, t3=2, D1=10, w=80, material="metal", n_fast=4, \
                                            length=200, offset=20,flange_height=80, \
                                            hole_coordinate_list=[(20, 10), (180, 30), (160, 20), (30, 30)], \
                                           D2_list=[10, 5, 9, 8], yieldstrength=83,N_lugs=1,N_Flanges=2)
loads_with_SF = DesignClass.Load(433.6,433.6,1300.81,817.34,817.34,0)
out1 = LocalLoadCalculatorAndLugDesignerAndLugConfigurator.Optimize_Lug(InputVariables.Material, \
                                                                 InputVariables.sigma_yield,InputVariables.Density,\
                                                                 initial_design, loads_with_SF, False)[0]
print(out1.h, out1.t1, out1.t2, out1.t3, out1.D1, out1.w, out1.length, out1.offset, out1.flange_height, out1.yieldstrength, out1.material)
out1.bottomplatewidth = out1.w
out2 = SelectFastenerConfiguration.Optimize_holes(out1, False)
#PostProcessorAndVisualizer.Visualize(initial_design)
PostProcessorAndVisualizer.Visualize2(out2)


