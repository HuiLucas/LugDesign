# This software component will return the results and provide a visualization in a graph. (maybe use the Inkscape
# package to make a 3-view)
import cadquery as cq
#import cadquery.cqgi as cqgi

from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

def Visualize(design_object):

    # make the base
    result = (
        cq.Workplane("XY")
        .box(design_object.w, design_object.length, design_object.t2)
        .faces(">Z")
        .workplane()
        .pushPoints(design_object.list_of_hole_center_coords)
        .hole(design_object.D2)
    )

    if design_object.w <= design_object.flange_height:
        filletrad = design_object.w / 2
    else:
        filletrad = design_object.flange_height / 2
    result = result.faces("<Y").workplane(
        offset=-design_object.offset
    )  # workplane is offset from the object surface
    result = result.union(
        cq.Workplane("XZ").box(design_object.w, design_object.flange_height + filletrad, design_object.t1, centered=[True, False, True]).edges(
            "|Y").fillet(filletrad - 0.01).translate((0, 0, +design_object.t2 / 2 - filletrad)).center(0,
                                                                                                -filletrad + design_object.t2 / 2).rect(
            design_object.w, 2 * filletrad).cutThruAll().center(0, design_object.flange_height).circle(design_object.D1).cutThruAll().translate(
            (0, design_object.w / 2 - design_object.offset, 0)))
    result = result.union(
        cq.Workplane("XZ").box(design_object.w, design_object.flange_height + filletrad, design_object.t1, centered=[True, False, True]).edges(
            "|Y").fillet(filletrad - 0.01).translate((0, 0, +design_object.t2 / 2 - filletrad)).center(0,
                                                                                                -filletrad + design_object.t2 / 2).rect(
            design_object.w, 2 * filletrad).cutThruAll().center(0, design_object.flange_height).circle(design_object.D1).cutThruAll().translate(
            (0, design_object.w / 2 - design_object.offset - design_object.h, 0)))
    # Export
    cq.exporters.export(result, "result.stl")
    cq.exporters.export(result.section(), "result.dxf")
    cq.exporters.export(result, "result.step")

    # Create a new plot
    figure = pyplot.figure()
    axes = figure.add_subplot(131, projection='3d')
    axes.view_init(elev=0, azim=0, roll=0)
    axes2 = figure.add_subplot(132, projection='3d')
    axes2.view_init(elev=90, azim=0, roll=0)
    pyplot.title("A 3D STL file is generated in the main directory which \n can be viewed in other software")
    axes3 = figure.add_subplot(133, projection='3d')
    axes3.view_init(elev=0, azim=90, roll=0)

    # Load the STL files and add the vectors to the plot
    your_mesh = mesh.Mesh.from_file('result.stl')
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
    axes2.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
    axes3.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))

    # Auto scale to the mesh size
    scale = your_mesh.points.flatten()
    axes.auto_scale_xyz(scale, scale, scale)
    axes2.auto_scale_xyz(scale, scale, scale)
    axes3.auto_scale_xyz(scale, scale, scale)
    # Show the plot to the screen
    pyplot.show()