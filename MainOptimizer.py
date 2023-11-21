# This file will change the design based on the part checks. It will start from an initial design, then perform all
# the checks as written in the other software components, and improve the design if possible with iterations.

import CheckBearing, CheckThermalStress, CheckPullThrough, GlobalLoadsCalculator, InputVariables, \
    LocalLoadCalculatorAndLugDesignerAndLugConfigurator, PostProcessorAndVisualizer, SelectFastener, TradeOffComperator, DesignClass

import SelectFastenerConfiguration



initial_design = DesignClass.DesignInstance(5, 2, 2, 2, 2, 2, 5, "metal")
initial_design.n_fast = 3
