# This software component will check the given input design for Pull Through Failure.
import MainOptimizer

debug_design = MainOptimizer.DesignInstance(5, 2, 2, 2, 2, 2, 5, "metal")
def check_pull_through(design_object):
    failure = True
    return failure

print(check_pull_through(debug_design))