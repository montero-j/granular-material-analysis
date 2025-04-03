// Script de Gmsh para generar una malla de la "insertion face"

// Parámetros
radius_insertion = 0.0140;  // Radio de la "insertion face"
height_insertion = 0.06;  // Altura donde se ubicará la "insertion face"

// Crear puntos para la "insertion face"
num_points = 36; 
theta = 2 * Pi / num_points;
Point(1) = {0, 0, height_insertion}; // Centro de la "insertion face"
For i In {0:num_points-1}
    Point(2 + i) = {radius_insertion * Cos(i * theta), radius_insertion * Sin(i * theta), height_insertion};
EndFor

// Crear círculos para la "insertion face"
For i In {0:num_points-1}
    Circle(1 + i) = {2 + i, 1, 2 + (i + 1) % num_points};
EndFor

// Crear la superficie de la "insertion face"
Curve Loop(1) = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36};
Plane Surface(1) = {1};

// Refinamiento de la malla
Mesh.CharacteristicLengthMin = 0.01; // Mejor resolución
Mesh.CharacteristicLengthMax = 0.05; // Mejor resolución

// Generar la malla
Mesh 2;
