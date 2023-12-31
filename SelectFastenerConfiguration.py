# This software component will select the fastener configuration according to WP4.4.
# this checks if given w allows for the number and size of fastners given constraints
import copy

import DesignClass
import math
import numpy as np


debug_design = DesignClass.DesignInstance(h=30, t1=5, t2=10, t3=2, D1=10, w=80, material="metal", n_fast=4, \
                                            length=200, offset=20,flange_height=80, \
                                            hole_coordinate_list=[(22, 20), (180, 30), (160, 20), (25, 25)], \
                                           D2_list=[10, 5, 9, 8], yieldstrength=83,N_lugs=1,N_Flanges=2)

#check wether spacing constraints detailed in 4.4 are met, inp
# buts are list of coordinates and list of diameter sizes
def fastener_spacing_check(design_object):
    np_D2_list = np.array(design_object.D2_list)
    np_hole_coordinate_list = np.array(design_object.hole_coordinate_list)
    # these
    if True == True: #design_object.material == "metal": # for now we only consider metals
        lower_limit = 2 * np.max(np_D2_list)
        upper_limit = 3 * np.max(np_D2_list)

    elif design_object.material == "composite":
        lower_limit = 4 * np.max(np_D2_list)
        upper_limit = 5 * np.max(np_D2_list)

    #for loop checks wether the holes are within the margin of 2 * D2 from edges. For every hole
    for i in range(len(np_D2_list)):
        if np_hole_coordinate_list[i,0] <= 2 * np_D2_list[i] or design_object.length - np_hole_coordinate_list[i,0] <= 2 * np_D2_list[i]:
            #print("LengthMarginErr")
            if np_hole_coordinate_list[i,0] - 2 * np_D2_list[i] <= 0:
                #print(np_hole_coordinate_list[i,0], np_D2_list[i])
                #print("LengthMarginErr1")
                return False , i , np_hole_coordinate_list[i,0] - 2 * np_D2_list[i], "LengthMarginError"
            elif design_object.length - np_hole_coordinate_list[i,0] - 2 * np_D2_list[i] <=0:
                #print("LengthMarginErr2")
                return False , i , design_object.length - np_hole_coordinate_list[i,0]- 2 * np_D2_list[i] , "LengthMarginError"
        if np_hole_coordinate_list[i,1]  < 2 * np_D2_list[i] or design_object.bottomplatewidth - np_hole_coordinate_list[i,1] < 2 * np_D2_list[i]:
            if np_hole_coordinate_list[i,1] - 2 * np_D2_list[i] <= 0:
                return False , i , np_hole_coordinate_list[i,1] - 2 * np_D2_list[i] , "WidthMarginError"
            elif design_object.bottomplatewidth - np_hole_coordinate_list[i,1] - 2 * np_D2_list[i] <=0:
                return False , i , design_object.bottomplatewidth - np_hole_coordinate_list[i,1] - 2 * np_D2_list[i] , "WidthMarginError"
    #lower limit and upper limit are calculated based on the material and the for loop checks wether the center to
    #center constraint complies...
    for i in range(len(np_D2_list)):
        for k in range(i + 1, len(np_D2_list)):
            distance_x = np_hole_coordinate_list[i][0] - np_hole_coordinate_list[k][0]
            distance_y = np_hole_coordinate_list[i][1] - np_hole_coordinate_list[k][1]
            distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
            if i != k and not distance >= lower_limit:
                # returns the indexs of the hole_list that are causing an issue and wether the distance betweeen them
                # should be increased or decreased
                return False, i, k, "HoleDistanceTooSmall"
            # elif i != k and not distance <= upper_limit:
            #     return False, i , k , "HoleDistanceTooLarge"
    return [True]


def Optimize_holes(design_object, recursive):
    new_object = copy.deepcopy(design_object)
    if fastener_spacing_check(new_object)[0] == True:
        return new_object
    if fastener_spacing_check(new_object)[3] == "LengthMarginError" and new_object.length < 500:
        #print("LengthMarginError")
        new_object.length += 1
        for i in range(len(new_object.hole_coordinate_list)):
            new_object.hole_coordinate_list[i] = (new_object.hole_coordinate_list[i][0]+0.5, new_object.hole_coordinate_list[i][1])
        #print(new_object.length)
        return Optimize_holes(new_object, True)
    elif fastener_spacing_check(new_object)[3] == "WidthMarginError" and new_object.bottomplatewidth < 400:
        #print("WidthMarginError")
        new_object.bottomplatewidth += 1
        for i in range(len(new_object.hole_coordinate_list)):
            new_object.hole_coordinate_list[i] = (new_object.hole_coordinate_list[i][0], new_object.hole_coordinate_list[i][1]+0.5)
        #print(new_object.bottomplatewidth, new_object.hole_coordinate_list[0])
        #print(fastener_spacing_check(new_object))
        return Optimize_holes(new_object, True)
    elif fastener_spacing_check(new_object)[3] == "HoleDistanceTooSmall":
        index1 = fastener_spacing_check(new_object)[1]
        index2 = fastener_spacing_check(new_object)[2]
        if abs(new_object.hole_coordinate_list[index1][0] - new_object.hole_coordinate_list[index2][0]) >= abs(new_object.hole_coordinate_list[index1][1] - new_object.hole_coordinate_list[index2][1]):
            if new_object.hole_coordinate_list[index1][0] - new_object.hole_coordinate_list[index2][0] <= 0:
                new_object.hole_coordinate_list[index1] = (new_object.hole_coordinate_list[index1][0]-1, new_object.hole_coordinate_list[index1][1])
                new_object.hole_coordinate_list[index2] = (
                new_object.hole_coordinate_list[index2][0] + 1,
                new_object.hole_coordinate_list[index2][1])
            if new_object.hole_coordinate_list[index1][0] - new_object.hole_coordinate_list[index2][0] >= 0:
                new_object.hole_coordinate_list[index1] = (new_object.hole_coordinate_list[index1][0]+1, new_object.hole_coordinate_list[index1][1])
                new_object.hole_coordinate_list[index2] = (
                new_object.hole_coordinate_list[index2][0] - 1,
                new_object.hole_coordinate_list[index2][1])
        else:
            if new_object.hole_coordinate_list[index1][1] - new_object.hole_coordinate_list[index2][1] <= 0:
                new_object.hole_coordinate_list[index1] = (new_object.hole_coordinate_list[index1][0], new_object.hole_coordinate_list[index1][1]-1)
                new_object.hole_coordinate_list[index2] = (
                new_object.hole_coordinate_list[index2][0],
                new_object.hole_coordinate_list[index2][1]+1)
            if new_object.hole_coordinate_list[index1][1] - new_object.hole_coordinate_list[index2][1] >= 0:
                new_object.hole_coordinate_list[index1] = (new_object.hole_coordinate_list[index1][0], new_object.hole_coordinate_list[index1][1]+1)
                new_object.hole_coordinate_list[index2] = (
                new_object.hole_coordinate_list[index2][0],
                new_object.hole_coordinate_list[index2][1]-1)
        return Optimize_holes(new_object, True)
    else:
        #print(new_object.length, new_object.bottomplatewidth, "dit")
        return new_object


