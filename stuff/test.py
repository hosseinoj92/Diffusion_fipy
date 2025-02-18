from fipy import CellVariable, Gmsh2DIn3DSpace, GaussianNoiseVariable, Viewer, TransientTerm, DiffusionTerm, DefaultSolver
from fipy.tools import numerix
from fipy.viewers import MayaviClient
mesh = Gmsh2DIn3DSpace('''
    radius = 5.0;
    cellSize = 0.3;

    // create inner 1/8 shell
    Point(1) = {0, 0, 0, cellSize};
    Point(2) = {-radius, 0, 0, cellSize};
    Point(3) = {0, radius, 0, cellSize};
    Point(4) = {0, 0, radius, cellSize};
    Circle(1) = {2, 1, 3};
    Circle(2) = {4, 1, 2};
    Circle(3) = {4, 1, 3};
    Line Loop(1) = {1, -3, 2} ;
    Ruled Surface(1) = {1};

    // create remaining 7/8 inner shells
    t1[] = Rotate {{0,0,1},{0,0,0},Pi/2} {Duplicata{Surface{1};}};
    t2[] = Rotate {{0,0,1},{0,0,0},Pi} {Duplicata{Surface{1};}};
    t3[] = Rotate {{0,0,1},{0,0,0},Pi*3/2} {Duplicata{Surface{1};}};
    t4[] = Rotate {{0,1,0},{0,0,0},-Pi/2} {Duplicata{Surface{1};}};
    t5[] = Rotate {{0,0,1},{0,0,0},Pi/2} {Duplicata{Surface{t4[0]};}};
    t6[] = Rotate {{0,0,1},{0,0,0},Pi} {Duplicata{Surface{t4[0]};}};
    t7[] = Rotate {{0,0,1},{0,0,0},Pi*3/2} {Duplicata{Surface{t4[0]};}};

    // create entire inner and outer shell
    Surface Loop(100)={1,t1[0],t2[0],t3[0],t7[0],t4[0],t5[0],t6[0]};
''', overlap=2).extrude(extrudeFunc=lambda r: 1.1 * r) 
phi = CellVariable(name = r"$\phi$", mesh = mesh)

phi.setValue(GaussianNoiseVariable(mesh=mesh,
    mean=0.5,
    variance = 0.01))
    


if __name__ == "__main__":
    try:
        viewer = MayaviClient(vars=phi,
                              datamin=0., datamax=1.,
                              daemon_file="sphereDaemon.py")
    except:
        viewer = Viewer(vars=phi,
                        datamin=0., datamax=1.,
                        xmin=-2.5, zmax=2.5)
        

PHI = phi.arithmeticFaceValue 
D = a = epsilon = 1.
eq = (TransientTerm()
      == DiffusionTerm(coeff=D * a**2 * (1 - 6 * PHI * (1 - PHI)))
      - DiffusionTerm(coeff=(D, epsilon**2))) 


dexp = -5
elapsed = 0.
if __name__ == "__main__":
    duration = 1000.
else:
    duration = 1e-2
while elapsed < duration:
    dt = min(100, numerix.exp(dexp))
    elapsed += dt
    dexp += 0.01
    eq.solve(phi, dt=dt, solver=DefaultSolver(precon=None)) 
    if __name__ == "__main__":
        viewer.plot()