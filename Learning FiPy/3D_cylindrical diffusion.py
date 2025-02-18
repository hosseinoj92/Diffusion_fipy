import numpy as np
import matplotlib.pyplot as plt

from fipy import (
    CellVariable, FaceVariable, TransientTerm,
    DiffusionTerm, UpwindConvectionTerm, Gmsh3D
)
from fipy.tools import numerix

# --- Define cylinder parameters ---
cellSize = 0.1
radius = 1.0
height = 3.0

# --- Create a cylindrical mesh using Gmsh3D ---
mesh = Gmsh3D('''
SetFactory("OpenCASCADE");
cellSize = %(cellSize)g;
radius = %(radius)g;
height = %(height)g;
Cylinder(1) = {0, 0, 0, 0, 0, height, radius};
Mesh.CharacteristicLengthFactor = cellSize;
''' % locals())

# --- Define the concentration variable ---
phi = CellVariable(name="Concentration", mesh=mesh, value=0.0)

# --- Initial droplet placement ---
# Place a cylindrical "droplet" at the center of the base with a smaller radius,
# affecting cells near the center of the cylinder.
droplet_radius = 0.5  
x, y, z = mesh.cellCenters
phi.setValue(5.0, where=(x**2 + y**2) < droplet_radius**2)

# --- Diffusion coefficient and buoyancy parameters ---
D = 1.0
gravity = 1.0

# Create a FaceVariable with 3 components (x, y, z)
velocity = FaceVariable(mesh=mesh, rank=1, value=(0.0, 0.0, 0.0))
# For a buoyancy effect, we adjust the z-component (vertical direction)
velocity[2] = -gravity * (phi.faceValue - 2.5)

# --- Define the PDE ---
eq = (TransientTerm(var=phi) ==
      DiffusionTerm(var=phi, coeff=D) -
      UpwindConvectionTerm(var=phi, coeff=velocity))

# --- Prepare a 2D slice for visualization ---
# We'll take a horizontal slice at mid-height (z ~ height/2)
tol = cellSize * 1.5
sliceMask = np.abs(z - height/2) < tol

plt.figure(figsize=(6,6))

# --- Time stepping ---
dt = 1
steps = 5

for step in range(steps):
    eq.solve(var=phi, dt=dt)
    
    # Update velocity field
    velocity[2] = -gravity * (phi.faceValue - 2.5)
    
    # Update the plot for the mid-height slice
    plt.clf()
    sc = plt.scatter(x[sliceMask], y[sliceMask],
                     c=phi.value[sliceMask],
                     cmap='viridis', vmin=0, vmax=5)
    plt.colorbar(sc)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"Cylindrical case, Step {step+1} (t = {(step+1)*dt:.2f} s)")
    plt.pause(0.5)

plt.show()
