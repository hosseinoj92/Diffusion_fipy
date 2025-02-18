// circle.geo
cellSize = 0.05;
radius = 1.0;

// Define center and four points on the circle (order matters)
Point(1) = {0, 0, 0, cellSize};
Point(2) = {-radius, 0, 0, cellSize};
Point(3) = {0, radius, 0, cellSize};
Point(4) = {radius, 0, 0, cellSize};
Point(5) = {0, -radius, 0, cellSize};

// Define four circular arcs using the center point:
Circle(6) = {2, 1, 3};  // from left to top
Circle(7) = {3, 1, 4};  // from top to right
Circle(8) = {4, 1, 5};  // from right to bottom
Circle(9) = {5, 1, 2};  // from bottom back to left

// Create a closed line loop and a plane surface
Line Loop(10) = {6, 7, 8, 9};
Plane Surface(11) = {10};
