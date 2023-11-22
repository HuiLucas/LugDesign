# This software component will check the given input design for Pull Through Failure.
import DesignClass


debug_design = DesignClass.DesignInstance(30, 5, 10, 2, 10,12, 80,"metal",4,100,20,80, [(-20, -30), (20, 30), (-10, 30), (20, -20)])
def check_pull_through(design_object):
    failure = True
    return failure

print(check_pull_through(debug_design))