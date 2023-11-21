# This file will change the design based on the part checks. It will start from an initial design, then perform all
# the checks as written in the other software components, and improve the design if possible with iterations.

import CheckBearing, CheckThermalStress, CheckPullThrough, GlobalLoadsCalculator, InputVariables, \
    LocalLoadCalculatorAndLugDesignerAndLugConfigurator, PostProcessorAndVisualizer, SelectFastener, TradeOffComperator, DesignClass

import SelectFastenerConfiguration

from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot




initial_design = DesignClass.DesignInstance(30, 5, 10, 2, 10, 12, 80, "metal")
initial_design.n_fast = 4
initial_design.width = 80
initial_design.offset = 20
initial_design.flange_height = 80
initial_design.list_of_hole_center_coords = [(-20, -30), (20, 30), (-10, 30), (20, -20)]
PostProcessorAndVisualizer.Visualize(initial_design)

# Create a new plot
figure = pyplot.figure()
axes = figure.add_subplot(131,projection='3d')
axes.view_init(elev=0, azim=0, roll=0)
axes2 = figure.add_subplot(132,projection='3d')
axes2.view_init(elev=90, azim=0, roll=0)
pyplot.title("A 3D STL file is generated in the main directory which \n can be viewed in other software")
axes3 = figure.add_subplot(133,projection='3d')
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