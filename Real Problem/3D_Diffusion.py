import os
import time
import numpy as np

from fipy import CellVariable, Grid3D, TransientTerm, DiffusionTerm
from mayavi import mlab
import imageio
from tqdm import tqdm

# Import the concrete GMRES solver class from FiPy
from fipy.solvers.petsc.linearGMRESSolver import LinearGMRESSolver

# -----------------------------
# Offscreen Rendering
# -----------------------------
mlab.options.offscreen = True

# -----------------------------
# Domain and Mesh Setup
# -----------------------------
domain_length = 10.0
nx = ny = nz = 10
dx = dy = dz = domain_length / nx

mesh = Grid3D(nx=nx, ny=ny, nz=nz, dx=dx, dy=dy, dz=dz)

# -----------------------------
# Cell Variable Setup
# -----------------------------
phi = CellVariable(name="Acid Concentration", mesh=mesh, value=0.0)

# Define a small acid droplet at the center
droplet_diameter = 1.0
droplet_radius = droplet_diameter / 2.0
center = domain_length / 2.0

x, y, z = mesh.cellCenters
phi.setValue(
    1.0,
    where=((x - center)**2 + (y - center)**2 + (z - center)**2 < droplet_radius**2)
)

# -----------------------------
# Diffusion Equation
# -----------------------------
D = 1.0  # diffusion coefficient
eq = TransientTerm() == DiffusionTerm(coeff=D)

# -----------------------------
# Frame Directory
# -----------------------------
frames_dir = "frames"
if not os.path.exists(frames_dir):
    os.makedirs(frames_dir)

# -----------------------------
# Visualization Function
# -----------------------------
def plot_phi(phi, step, dt):
    """
    Renders a 3D contour plot of the concentration field using Mayavi,
    then saves each frame as a PNG for animation.
    """
    # Reshape FiPy's 1D data array into 3D
    data = phi.value.reshape((nx, ny, nz))
    
    # Create coordinate arrays for the domain
    X, Y, Z = np.mgrid[
        0 : domain_length : complex(0, nx),
        0 : domain_length : complex(0, ny),
        0 : domain_length : complex(0, nz)
    ]
    
    mlab.clf()  # clear the figure
    mlab.contour3d(X, Y, Z, data, contours=10, opacity=0.5, colormap="viridis")
    mlab.outline(color=(0, 0, 0))
    mlab.title(f"t = {step * dt:.1f} s", size=0.5)
    
    # Save the frame
    filename = os.path.join(frames_dir, f"frame_{step:04d}.png")
    mlab.savefig(filename)
    mlab.process_ui_events()

# -----------------------------
# Time-Stepping Parameters
# -----------------------------
dt = 1
steps = 5

# -----------------------------
# Concrete PETSc Solver
# -----------------------------
solver = LinearGMRESSolver(tolerance=1e-8, iterations=1000)

# -----------------------------
# Main Simulation Loop
# -----------------------------
start_time = time.time()
for step in tqdm(range(steps), desc="Simulating"):
    eq.solve(var=phi, dt=dt, solver=solver)
    plot_phi(phi, step, dt)
    
    if step % 10 == 0:
        elapsed = time.time() - start_time
        print(f"Step {step} completed. Elapsed: {elapsed:.2f}s")

mlab.close(all=True)

# -----------------------------
# Create Animated GIF
# -----------------------------
filenames = sorted([
    os.path.join(frames_dir, f)
    for f in os.listdir(frames_dir)
    if f.endswith(".png")
])
images = [imageio.imread(fn) for fn in filenames]
gif_filename = "diffusion.gif"
imageio.mimsave(gif_filename, images, duration=0.1)

print(f"Animation complete. GIF saved as {gif_filename}")
