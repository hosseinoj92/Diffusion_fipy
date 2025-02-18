from fipy import *
from fipy import CellVariable, Gmsh2D, TransientTerm, DiffusionTerm, Viewer
from numpy import random
cellSize = 0.05
radius = 1
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

phi = CellVariable(name="solution variable",
                   mesh=mesh,
                   value=0.)

viewer = None
from fipy import input

if __name__ == '__main__':
    try:
        viewer = Viewer(vars=phi, datamin=-1, datamax=1.)
        viewer.plotMesh(mesh)
        # input("Irregular circular mesh. Press <return> to proceed")  # doctest: +GMSH
    except:
        print("Unable to create a viewer for an irregular mesh (try Matplotlib2DViewer or MayaviViewer)")



D = 1.

X, Y = mesh.faceCenters
phi.constrain(2, mesh.facesLeft)
phi.constrain(2, mesh.facesTop)
timeStepDuration = 10 * 0.9 * cellSize ** 2 / (2 * D)

steps = 200
Temp = 5 * random.sample(steps) + 20

phi.setValue(0.5)
for step in range(steps):

    k = -200 * 10 ** (20 - Temp[step])

    eq = TransientTerm() + PowerLawConvectionTerm([step%4,-step]) == DiffusionTerm(coeff=D) + ImplicitSourceTerm(coeff=k)
    eq.solve(var=phi,
             dt=timeStepDuration)

    print(phi._getValue())
    if viewer is not None:
        viewer.plot()
