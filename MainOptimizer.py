# This file will change the design based on the part checks. It will start from an initial design, then perform all
# the checks as written in the other software components, and improve the design if possible with iterations.

import CheckBearing, CheckThermalStress, CheckPullThrough, GlobalLoadsCalculator, InputVariables, \
    LocalLoadCalculatorAndLugDesignerAndLugConfigurator, PostProcessorAndVisualizer, SelectFastener, TradeOffComperator, \
    DesignClass

import SelectFastenerConfiguration


initial_design = DesignClass.DesignInstance(h=30, t1=5, t2=10, t3=2, D1=10, D2=12, w=80, material="metal", n_fast=4, \
                                            length=100, offset=20,flange_height=80, \
                                            list_of_hole_center_coords=[(-20, -30), (20, 30), (-10, 30), (20, -20)])
PostProcessorAndVisualizer.Visualize(initial_design)


