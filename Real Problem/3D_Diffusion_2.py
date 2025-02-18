from fipy import *
import mayavi.mlab as mlab
import numpy as np
import time
from fipy import CellVariable, Grid3D, TransientTerm, DiffusionTerm

# Spatial parameters
nx = ny = nz = 30
dx = dy = dz = 1
L = nx * dx

# Diffusion and time step
D = 1.
dt = 10.0 * dx**2 / (2. * D)
steps = 4

# Initial value and radius of concentration
phi0 = 1.0
r = 3.0

# Rates
alpha = 1.0  # Source coefficient
gamma = 0.01 # Sink coefficient

mesh = Grid3D(nx=nx, ny=ny, nz=nz, dx=dx, dy=dy, dz=dz)
X, Y, Z = mesh.cellCenters
phi = CellVariable(mesh=mesh, name=r"$\phi$", value=0.)

src = phi * alpha  # source term
degr = -gamma * phi  # sink term

eq = TransientTerm() == DiffusionTerm(coeff=D) + src + degr

# Initial concentration: a sphere in the center
phi.setValue(1.0, where=((X - nx/2)**2 + (Y - ny/2)**2 + (Z - nz/2)**2 < r**2))

# Solve
start_time = time.time()
results = [phi.value.copy()]  # Use phi.value
for step in range(steps):
    eq.solve(var=phi, dt=dt)
    results.append(phi.value.copy())  # Use phi.value
print('Time elapsed:', time.time() - start_time)

# Plot each time step
for i, res in enumerate(results):
    fig = mlab.figure()
    res3D = res.reshape(nx, ny, nz)

    mlab.contour3d(res3D, opacity=0.3, vmin=0, vmax=1, contours=100, 
                   transparent=True, extent=[0, 10, 0, 10, 0, 10])
    mlab.colorbar()
    mlab.savefig(f'diffusion3d_{i+1}.png')
    mlab.close()
