# This software component will return the results and provide a visualization in a graph. (maybe use the Inkscape
# package to make a 3-view)
import cadquery as cq
#import cadquery.cqgi as cqgi

def Visualize(design_object):

    # make the base
    result = (
        cq.Workplane("XY")
        .box(design_object.w, design_object.width, design_object.t2)
        .faces(">Z")
        .workplane()
        .pushPoints(design_object.list_of_hole_center_coords)
        .hole(design_object.D2)
    )

    if design_object.width <= design_object.flange_height:
        filletrad = design_object.width / 2
    else:
        filletrad = design_object.flange_height / 2
    result = result.faces("<Y").workplane(
        offset=-design_object.offset
    )  # workplane is offset from the object surface
    result = result.union(
        cq.Workplane("XZ").box(design_object.width, design_object.flange_height + filletrad, design_object.t1, centered=[True, False, True]).edges(
            "|Y").fillet(filletrad - 0.01).translate((0, 0, +design_object.t2 / 2 - filletrad)).center(0,
                                                                                                -filletrad + design_object.t2 / 2).rect(
            design_object.width, 2 * filletrad).cutThruAll().center(0, design_object.flange_height).circle(design_object.D1).cutThruAll().translate(
            (0, design_object.w / 2 - design_object.offset, 0)))
    result = result.union(
        cq.Workplane("XZ").box(design_object.width, design_object.flange_height + filletrad, design_object.t1, centered=[True, False, True]).edges(
            "|Y").fillet(filletrad - 0.01).translate((0, 0, +design_object.t2 / 2 - filletrad)).center(0,
                                                                                                -filletrad + design_object.t2 / 2).rect(
            design_object.width, 2 * filletrad).cutThruAll().center(0, design_object.flange_height).circle(design_object.D1).cutThruAll().translate(
            (0, design_object.w / 2 - design_object.offset - design_object.h, 0)))
    # Export
    cq.exporters.export(result, "result.stl")
    cq.exporters.export(result.section(), "result.dxf")
    cq.exporters.export(result, "result.step")