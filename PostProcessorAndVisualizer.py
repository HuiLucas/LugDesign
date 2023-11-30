# This software component will return the results and provide a visualization in a graph. (maybe use the Inkscape
# package to make a 3-view)
import cadquery as cq
import DesignClass
#import cadquery.cqgi as cqgi

from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

def Visualize(design_object, move_y=0):
    for i in range(len(design_object.hole_coordinate_list)):
        a = design_object.hole_coordinate_list[i][0]
        design_object.hole_coordinate_list[i] = (
        design_object.hole_coordinate_list[i][1] - design_object.bottomplatewidth / 2, a - design_object.length / 2)
        # make the base
    result = (
        cq.Workplane("XY")
        .box(design_object.bottomplatewidth, design_object.length, design_object.t2).faces(">Z").workplane().tag("noholes")
    )

    for i in range(len(design_object.D2_list)):
        result = result.workplaneFromTagged("noholes").pushPoints(design_object.hole_coordinate_list[i:i + 1]).hole(
            design_object.D2_list[i])

    if design_object.w <= design_object.flange_height:
        filletrad = design_object.w / 2
    else:
        filletrad = design_object.flange_height / 2
    result = result.faces("<Y").workplane(
        offset=-design_object.offset
    )  # workplane is offset from the object surface
    result = result.union(
        cq.Workplane("XZ").box(design_object.w, design_object.flange_height + filletrad, design_object.t1,
                               centered=[True, False, True]).edges(
            "|Y").fillet(filletrad - 0.01).translate((0, 0, +design_object.t2 / 2 - filletrad)).center(0,
                                                                                                       -filletrad + design_object.t2 / 2).rect(
            design_object.w, 2 * filletrad).cutThruAll().center(0, design_object.flange_height).circle(
            design_object.D1/2).cutThruAll().translate(
            (0, design_object.w / 2 - design_object.offset, 0)))
    if design_object.N_Flanges == 2:
        result = result.union(
            cq.Workplane("XZ").box(design_object.w, design_object.flange_height + filletrad, design_object.t1,
                                   centered=[True, False, True]).edges(
                "|Y").fillet(filletrad - 0.01).translate((0, 0, +design_object.t2 / 2 - filletrad)).center(0,
                                                                                                           -filletrad + design_object.t2 / 2).rect(
                design_object.w, 2 * filletrad).cutThruAll().center(0, design_object.flange_height).circle(
                design_object.D1/2).cutThruAll().translate(
                (0, design_object.w / 2 - design_object.offset - design_object.h, 0)))
    if design_object.N_lugs == 2:
        result = result.union(result.translate((0,move_y, 0)))
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

def Visualize2(design_object):
    Visualize(design_object)
    if design_object.N_lugs == 2:
        Visualize(design_object, move_y=design_object.Dist_between_lugs)

# debug_design4 = DesignClass.DesignInstance(h=30, t1=5, t2=10, t3=2, D1=10, w=80, material="metal", n_fast=4, \
#                                             length=200, offset=20,flange_height=80, \
#                                             hole_coordinate_list=[(20, 10), (180, 30), (160, 20), (30, 30)], \
#                                            D2_list=[10, 5, 9, 8], yieldstrength=83,N_lugs=2,N_Flanges=1)
# debug_design4.Dist_between_lugs = 300
# Visualize2(debug_design4)