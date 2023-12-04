# This software component will do the whole analysis for two different materials, and then compare them.
def TradeOff(design_array2):
    for design in design_array2:
        print(f"{design.material}")
        print(f"checklist: {design.checklist}, h: {design.h}, t1: {design.t1}, t2: {design.t2}, t3: {design.t3}, D1: {design.D1}, w: {design.w}, length: {design.length}, offset: {design.offset}, flange height: {design.flange_height}, yieldstrength: {design.yieldstrength}, material: {design.material}, Dist_between_lugs: {design.Dist_between_lugs}, N_lugs: {design.N_lugs}, N_Flanges: {design.N_Flanges}, hole coords: {design.hole_coordinate_list}, n_fast: {design.n_fast}, D2holes: {design.D2_list}, bottomplatewidth: {design.bottomplatewidth}, shearstrength: {design.shearstrength}")
        print(f"nut type: {design.fasteners.nut_type}, hole type: {design.fasteners.hole_type}, material: {design.fasteners.material}")
        print(f"mass: {design.mass}")
        print("")

    # add comparison/trade-off here