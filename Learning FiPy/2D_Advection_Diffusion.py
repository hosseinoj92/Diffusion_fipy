import numpy as np
import matplotlib.pyplot as plt

# FiPy imports
from fipy import (
    CellVariable, FaceVariable,
    Grid2D, TransientTerm,
    DiffusionTerm, UpwindConvectionTerm
)

# --- Domain setup ---
domain_length = 10.0  # mm
nx, ny = 100, 100
dx = domain_length / nx
dy = domain_length / ny
mesh = Grid2D(nx=nx, ny=ny, dx=dx, dy=dy)

# --- Define acid concentration variable ---
phi = CellVariable(name="Acid Concentration", mesh=mesh, value=0.0)

# --- Initial droplet placement ---
droplet_radius = 1.0  # mm
center_x, center_y = domain_length / 2, domain_length / 2
x, y = mesh.cellCenters
phi.setValue(5.0, where=((x - center_x)**2 + (y - center_y)**2) < droplet_radius**2)

# --- Diffusion coefficient ---
D = 1.0  # mm²/s

# --- Buoyancy-driven velocity field (simplified) ---
gravity = 1.0  # "strength" of buoyancy effect

# 
# IMPORTANT: Create a single FaceVariable with rank=1
# This will hold velocity components in the x (index=0) and y (index=1) directions.
#
velocity = FaceVariable(mesh=mesh, rank=1, value=(0.0, 0.0))

#
# We'll define velocity[1] (the y-component) based on concentration.
# This is a toy Boussinesq approach, so heavier fluid sinks (concentration above 2.5) 
# and lighter fluid rises (concentration below 2.5).
#
velocity[1] = -gravity * (phi.faceValue - 2.5)  # negative => goes downward if phi > 2.5

#
# Define the PDE:  TransientTerm(phi) = DiffusionTerm(phi) - UpwindConvectionTerm(phi, velocity)
#
eq = (TransientTerm(var=phi) 
      == DiffusionTerm(var=phi, coeff=D)
      - UpwindConvectionTerm(var=phi, coeff=velocity))

# --- Set up the plot ---
fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(phi.value.reshape((ny, nx)),
               extent=(0, domain_length, 0, domain_length),
               origin='lower', cmap='viridis', vmin=0.2, vmax=1)
plt.colorbar(im, ax=ax)
ax.set_xlabel('x (mm)')
ax.set_ylabel('y (mm)')
plt.tight_layout()

# --- Time stepping ---
dt = 0.01
steps = 200

for step in range(steps):
    # Solve PDE
    eq.solve(var=phi, dt=dt)
    
    # Recalculate velocity field after phi has changed
    velocity[1] = -gravity * (phi.faceValue - 2.5)

    # Update plot
    im.set_data(phi.value.reshape((ny, nx)))
    ax.set_title(f"Diffusion + Convection (t = {step * dt:.2f} s)")
    plt.pause(0.05)

plt.show()
