// Define parameters
cellSize = 1.0;
L = 20.0;

// Define the four corner points of the rectangle
Point(1) = {0, 0, 0, cellSize};
Point(2) = {L, 0, 0, cellSize};
Point(3) = {L, L, 0, cellSize};
Point(4) = {0, L, 0, cellSize};

// Create lines for the boundary
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};

// Create a closed loop and a plane surface
Line Loop(5) = {1, 2, 3, 4};
Plane Surface(6) = {5};

