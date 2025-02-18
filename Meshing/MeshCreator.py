import gmsh

gmsh.initialize()
gmsh.open("Meshing/cylinder.geo")
gmsh.model.mesh.generate(3)

# Force msh2 output by setting the mesh file version to 2.2
gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)

gmsh.write("Meshing/cylinder.msh")
gmsh.finalize()

