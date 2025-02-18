SetFactory("OpenCASCADE");

// Define parameters
r = 1;        // Cylinder radius
h = 5;        // Cylinder height
lc = 0.1;     // Mesh characteristic length (rough control of element size)

// Create a cylinder
Cylinder(1) = {0, 0, 0, 0, 0, h, r};

// Tag the volume as a "Physical Volume" so FiPy can recognize it
Physical Volume("CylinderVolume") = {1};

// Optionally, set global mesh size constraints
Mesh.CharacteristicLengthMax = lc;
Mesh.CharacteristicLengthMin = lc;
