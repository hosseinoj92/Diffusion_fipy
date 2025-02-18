import numpy as np
import matplotlib.pyplot as plt
from fipy import CellVariable, Grid2D, TransientTerm, DiffusionTerm

# Define domain parameters (in mm)
domain_length = 10.0  # Domain is 10 mm x 10 mm
nx, ny = 100, 50     # Grid resolution
dx = domain_length / nx
dy = domain_length / ny

# Create a 2D grid mesh
mesh = Grid2D(nx=nx, ny=ny, dx=dx, dy=dy)

# Create a cell variable for the acid concentration; initialize to 0 (water)
phi = CellVariable(name="Acid Concentration", mesh=mesh, value=0.0)

# Define the acid droplet properties
droplet_diameter = 1.0  # mm
droplet_radius = droplet_diameter / 2.0  # mm

# Place the droplet at the center of the domain
center_x = domain_length / 2
center_y = domain_length / 2

# Get the coordinates of cell centers
x, y = mesh.cellCenters

# Set the initial condition: inside the droplet, concentration = 1 M (acid)
phi.setValue(5.0, where=((x - center_x)**2 + (y - center_y)**2) < droplet_radius**2)

# Diffusion coefficient (in mm^2/s); adjust as needed
D = 1.0

# Define the transient diffusion equation:
#   (∂phi/∂t) = D * ∇²phi
eq = TransientTerm() == DiffusionTerm(coeff=D)

# Set up a Matplotlib plot for real-time visualization
fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(phi.value.reshape((ny, nx)), extent=(0, domain_length, 0, domain_length),
               origin='lower', cmap='viridis', vmin=0, vmax=1)
plt.colorbar(im, ax=ax)
ax.set_xlabel('x (mm)')
ax.set_ylabel('y (mm)')
ax.set_title("Acid Diffusion at t = 0.0 s")
plt.tight_layout()

# Time-stepping parameters
dt = 0.01  # time step in seconds
steps = 200

# Run the simulation and update the plot
for step in range(steps):
    eq.solve(var=phi, dt=dt)
    # Update plot with new data (reshape phi.value to a 2D array)
    im.set_data(phi.value.reshape((ny, nx)))
    ax.set_title(f"Acid Diffusion at t = {step * dt:.1f} s")
    plt.pause(0.05)

plt.show()
