import gmsh
from math import pi

gmsh.initialize()
gmsh.option.setNumber("Mesh.SaveAll", 1)
gmsh.option.setNumber("Mesh.Algorithm", 6)
# Set the mesh file version to 2.2 for FiPy compatibility
gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)
gmsh.model.add("t1")
lc = 10e-3  # (Currently not used directly in geometry definition)

# Define geometry using the OCC kernel
gmsh.model.occ.addCircle(0.0, 0.0, 0.0, 100.0, 1, angle1=0., angle2=2*pi)
gmsh.model.occ.addCurveLoop([1], 2)
gmsh.model.occ.addPlaneSurface([2], 1)

# Synchronize the OCC model to create the internal CAD model
gmsh.model.occ.synchronize()

# Now define physical groups
gmsh.model.addPhysicalGroup(1, [1], 1)  # For the curve (1D)
gmsh.model.addPhysicalGroup(2, [1], 2)  # For the surface (2D)

# Generate the mesh and write to file
gmsh.model.mesh.generate(2)
gmsh.write("Circle.msh")
gmsh.finalize()
