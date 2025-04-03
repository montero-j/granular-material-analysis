import gmsh
import os
import math

def read_params(filename):
    params = {}
    with open(filename, "r") as f:
        for line in f:
            parts = line.split()
            if len(parts) == 4 and parts[0] == "variable":
                params[parts[1]] = float(parts[3])
    return params

def generate_silo(orifice_radius, base_radius=1.0, height=6.0, num_points=36, output_file="Silo.stl"):
    gmsh.initialize()
    gmsh.model.add("Silo")
    
    theta = 2 * math.pi / num_points
    
    # Orifice points
    gmsh.model.geo.addPoint(0, 0, 0, tag=1)
    for i in range(num_points):
        gmsh.model.geo.addPoint(orifice_radius * math.cos(i * theta), 
                                 orifice_radius * math.sin(i * theta), 0, tag=2 + i)
    
    # Base points
    for i in range(num_points):
        gmsh.model.geo.addPoint(base_radius * math.cos(i * theta), 
                                 base_radius * math.sin(i * theta), 0, tag=100 + i)
    
    # Top points
    for i in range(num_points):
        gmsh.model.geo.addPoint(base_radius * math.cos(i * theta), 
                                 base_radius * math.sin(i * theta), height, tag=200 + i)
    gmsh.model.geo.addPoint(0, 0, height, tag=300)
    
    # Curves
    for i in range(num_points):
        gmsh.model.geo.addCircleArc(2 + i, 1, 2 + (i + 1) % num_points, tag=1 + i)
        gmsh.model.geo.addCircleArc(100 + i, 1, 100 + (i + 1) % num_points, tag=100 + i)
        gmsh.model.geo.addCircleArc(200 + i, 300, 200 + (i + 1) % num_points, tag=200 + i)
        gmsh.model.geo.addLine(200 + i, 100 + i, tag=300 + i)
    
    # Create lateral surfaces
    for i in range(num_points):
        gmsh.model.geo.addCurveLoop([100 + i, 300 + i, -(200 + i), -(300 + (i + 1) % num_points)], tag=400 + i)
        gmsh.model.geo.addPlaneSurface([400 + i], tag=500 + i)
    
    # Create base with orifice
    gmsh.model.geo.addCurveLoop([i + 1 for i in range(num_points)], tag=1)  # Orifice
    gmsh.model.geo.addCurveLoop([100 + i for i in range(num_points)], tag=2)  # Base
    gmsh.model.geo.addPlaneSurface([2, -1], tag=3)  # Base with orifice removed
    
    
    # Create volume
    gmsh.model.geo.addSurfaceLoop([3] + [500 + i for i in range(num_points)], tag=6)

    
    gmsh.model.geo.synchronize()
    gmsh.model.mesh.generate(3)
    gmsh.write(output_file)
    gmsh.finalize()

def generate_lid(orifice_radius, num_points=36, output_file="Lid.stl"):
    gmsh.initialize()
    gmsh.model.add("Lid")
    
    theta = 2 * math.pi / num_points
    
    gmsh.model.geo.addPoint(0, 0, 0, tag=1)
    for i in range(num_points):
        gmsh.model.geo.addPoint(orifice_radius * math.cos(i * theta), 
                                 orifice_radius * math.sin(i * theta), 0, tag=2 + i)
    
    for i in range(num_points):
        gmsh.model.geo.addCircleArc(2 + i, 1, 2 + (i + 1) % num_points, tag=1 + i)
    
    gmsh.model.geo.addCurveLoop([1 + i for i in range(num_points)], tag=1)
    gmsh.model.geo.addPlaneSurface([1], tag=1)
    
    gmsh.model.geo.synchronize()
    gmsh.model.mesh.generate(2)
    gmsh.write(output_file)
    gmsh.finalize()

def generate_insertionsface(insertion_radius, height, num_points=36, output_file="Insertionsface.stl"):
    gmsh.initialize()
    gmsh.model.add("Insertionsface")
    
    theta = 2 * math.pi / num_points
    
    gmsh.model.geo.addPoint(0, 0, height, tag=1)
    for i in range(num_points):
        gmsh.model.geo.addPoint(insertion_radius * math.cos(i * theta), 
                                 insertion_radius * math.sin(i * theta), height, tag=2 + i)
    
    for i in range(num_points):
        gmsh.model.geo.addCircleArc(2 + i, 1, 2 + (i + 1) % num_points, tag=1 + i)
    
    gmsh.model.geo.addCurveLoop([1 + i for i in range(num_points)], tag=1)
    gmsh.model.geo.addPlaneSurface([1], tag=1)
    
    gmsh.model.geo.synchronize()
    gmsh.model.mesh.generate(2)
    gmsh.write(output_file)
    gmsh.finalize()

def main():
    params = read_params("sim.params")
    orifice_radius = params.get("Orifice_radius", 0.1345)
    insertion_radius = 1.0  # Valor fijo correcto
    height = 6.0  # Valor fijo correcto
    
    generate_silo(orifice_radius)
    generate_lid(orifice_radius)
    generate_insertionsface(insertion_radius, height)

if __name__ == "__main__":
    main()

