# This file will change the design based on the part checks. It will start from an initial design, then perform all
# the checks as written in the other software components, and improve the design if possible with iterations.

import CheckBearing, CheckThermalStress, CheckPullThrough, GlobalLoadsCalculator, InputVariables, \
    LocalLoadCalculatorAndLugDesignerAndLugConfigurator, PostProcessorAndVisualizer, SelectFastener, \
    SelectFastenerConfiguration, TradeOffComperator


class DesignInstance:
    def __init__(self, h, t1, t2, t3, D1, D2, w):
        self.h = h
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.D1 = D1
        self.D2 = D2
        self.w = w


initial_design = DesignInstance(5, 2, 2, 2, 2, 2, 5)
