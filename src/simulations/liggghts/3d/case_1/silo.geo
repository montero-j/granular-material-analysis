// Script de Gmsh para generar un silo 3D con base plana y un orificio en el centro

// Parámetros
radius_orifice = 0.0015;  // Radio del orificio de descarga
radius_base = 0.015;    // Radio de la base del silo
height_silo = 0.06;      // Altura del silo

// Crear puntos para el orificio
num_points = 36; 
theta = 2 * Pi / num_points;
Point(1) = {0, 0, 0}; // Centro del orificio
For i In {0:num_points-1}
    Point(2 + i) = {radius_orifice * Cos(i * theta), radius_orifice * Sin(i * theta), 0};
EndFor

// Crear puntos para la base
For i In {0:num_points-1}
    Point(100 + i) = {radius_base * Cos(i * theta), radius_base * Sin(i * theta), 0};
EndFor

// Crear puntos para el techo
For i In {0:num_points-1}
    Point(200 + i) = {radius_base * Cos(i * theta), radius_base * Sin(i * theta), height_silo};
EndFor
Point(300) = {0, 0, height_silo}; // Centro del techo

// Crear círculos para el orificio
For i In {0:num_points-1}
    Circle(1 + i) = {2 + i, 1, 2 + (i + 1) % num_points};
EndFor

// Crear círculos para la base
For i In {0:num_points-1}
    Circle(100 + i) = {100 + i, 1, 100 + (i + 1) % num_points};
EndFor

// Crear círculos para el techo
For i In {0:num_points-1}
    Circle(200 + i) = {200 + i, 300, 200 + (i + 1) % num_points};
EndFor

// Crear líneas verticales del silo
For i In {0:num_points-1}
    Line(300 + i) = {200 + i, 100 + i};
EndFor

// Crear la base del silo restando el orificio
Curve Loop(1) = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36}; // Orificio
Curve Loop(2) = {100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135}; // Base del silo
Plane Surface(1) = {2, 1}; // Base con orificio restado

// Crear el techo del silo
Curve Loop(3) = {200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235};
// Plane Surface(2) = {3};

// Crear superficies laterales del silo
For i In {0:num_points-1}
    Curve Loop(300 + i) = {100 + i, 300 + i, -(200 + i), -(300 + ((i + 1) % num_points))};
    Plane Surface(100 + i) = {300 + i};
EndFor

// Crear el volumen del silo
Surface Loop(1) = {1, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135};
Volume(1) = {1};

// Refinamiento de la malla
Mesh.CharacteristicLengthMin = 0.05; // Mejor resolución
Mesh.CharacteristicLengthMax = 0.2;  // Mejor resolución

// Generar la malla
Mesh 2;
