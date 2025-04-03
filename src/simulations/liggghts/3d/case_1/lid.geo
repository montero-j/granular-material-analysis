// Script de Gmsh para generar una malla del tamaño del orificio de descarga

// Parámetros
radius_orifice = 0.0015;  // Radio del orificio de descarga

// Crear puntos para el orificio
num_points = 36; 
theta = 2 * Pi / num_points;
Point(1) = {0, 0, 0}; // Centro del orificio
For i In {0:num_points-1}
    Point(2 + i) = {radius_orifice * Cos(i * theta), radius_orifice * Sin(i * theta), 0};
EndFor

// Crear círculos para el orificio
For i In {0:num_points-1}
    Circle(1 + i) = {2 + i, 1, 2 + (i + 1) % num_points};
EndFor

// Crear la superficie del orificio
Curve Loop(1) = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36};
Plane Surface(1) = {1};

// Refinamiento de la malla
Mesh.CharacteristicLengthMin = 0.01; // Mejor resolución
Mesh.CharacteristicLengthMax = 0.05; // Mejor resolución

// Generar la malla
Mesh 2;
