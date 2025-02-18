import numpy as np
import matplotlib.pyplot as plt

# FiPy imports
from fipy import (
    CellVariable, FaceVariable,
    TransientTerm, DiffusionTerm, UpwindConvectionTerm,
    Gmsh2D, Viewer
)
from fipy.tools import numerix

# --- Create a circular mesh using Gmsh2D ---
cellSize = 0.05
radius = 3.0
mesh = Gmsh2D('''
              cellSize = %(cellSize)g;
              radius = %(radius)g;
              Point(1) = {0, 0, 0, cellSize};
              Point(2) = {-radius, 0, 0, cellSize};
              Point(3) = {0, radius, 0, cellSize};
              Point(4) = {radius, 0, 0, cellSize};
              Point(5) = {0, -radius, 0, cellSize};
              Circle(6) = {2, 1, 3};
              Circle(7) = {3, 1, 4};
              Circle(8) = {4, 1, 5};
              Circle(9) = {5, 1, 2};
              Line Loop(10) = {6, 7, 8, 9};
              Plane Surface(11) = {10};
              ''' % locals())

# --- Define the acid concentration variable ---
phi = CellVariable(name="Acid Concentration", mesh=mesh, value=0.0)

# --- Initial droplet placement ---
# Here the droplet is placed at the center (0,0) of the circular domain.
droplet_radius = 0.5  # choose a radius smaller than the domain's radius
x, y = mesh.cellCenters
phi.setValue(5.0, where=(x**2 + y**2) < droplet_radius**2)

# --- Diffusion coefficient ---
D = 1.0  # mm²/s

# --- Buoyancy-driven velocity field (simplified) ---
gravity = 1.0  # strength of buoyancy effect

# Create a single FaceVariable with rank=1 (holds both x and y components)
velocity = FaceVariable(mesh=mesh, rank=1, value=(0.0, 0.0))
# For this toy model, we define the vertical component based on phi.
# (Here we let regions with high phi drive a downward motion.)
velocity[1] = -gravity * (phi.faceValue - 2.5)

# --- Define the PDE ---
eq = (TransientTerm(var=phi) ==
      DiffusionTerm(var=phi, coeff=D) -
      UpwindConvectionTerm(var=phi, coeff=velocity))

# --- Set up the Viewer ---
# This viewer will display the evolving field on the circular mesh.
viewer = Viewer(vars=phi, datamin=0, datamax=3)
viewer.plotMesh()  # Optionally display the mesh structure

# --- Time stepping ---
dt = 0.01
steps = 500

for step in range(steps):
    # Solve the PDE for one time step
    eq.solve(var=phi, dt=dt)
    
    # Recalculate the velocity field after phi has changed.
    velocity[1] = -gravity * (phi.faceValue - 2.5)
    
    # Update the viewer with the new solution.
    viewer.plot()

# Hold the final plot (in some environments, you may need to close the window manually)
input("Simulation complete. Press Enter to exit.")
