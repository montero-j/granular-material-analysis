import gmsh


def read_params(filename):
    params = {}
    with open(filename, "r") as f:
        for line in f:
            parts = line.split()
            if len(parts) == 4 and parts[0] == "variable":
                params[parts[1]] = float(parts[3])
    return params


def generate_silo(orifice_width, orifice_height, base_width, base_height, height, num_points=4, num_layers=1):
    gmsh.initialize()
    gmsh.model.add("Silo")

    layer_height = height / num_layers

    base_points = [
        (base_width / 2, -base_height / 2),
        (base_width / 2, base_height / 2),
        (-base_width / 2, base_height / 2),
        (-base_width / 2, -base_height / 2)
    ]

    def create_layer(z, base_tag_offset):
        return [gmsh.model.geo.addPoint(x, y, z, tag=base_tag_offset + i) for i, (x, y) in enumerate(base_points)]

    def create_orifice(z, base_tag_offset):
        orifice_points = [
            (orifice_width / 2, -orifice_height / 2),
            (orifice_width / 2, orifice_height / 2),
            (-orifice_width / 2, orifice_height / 2),
            (-orifice_width / 2, -orifice_height / 2)
        ]
        return [gmsh.model.geo.addPoint(x, y, z, tag=base_tag_offset + i) for i, (x, y) in enumerate(orifice_points)]

    orifice_tags = create_orifice(0, 100)
    base_tags = create_layer(0, 200)
    layer_tags = [create_layer(i * layer_height, 300 + i * 100) for i in range(1, num_layers)]
    top_tags = create_layer(height, 300 + num_layers * 100)

    orifice_curves = [gmsh.model.geo.addLine(orifice_tags[i], orifice_tags[(i + 1) % num_points]) for i in range(num_points)]
    base_curves = [gmsh.model.geo.addLine(base_tags[i], base_tags[(i + 1) % num_points]) for i in range(num_points)]
    top_curves = [gmsh.model.geo.addLine(top_tags[i], top_tags[(i + 1) % num_points]) for i in range(num_points)]
    
    vertical_curves = []
    horizontal_curves = []
    previous_layer = base_tags
    for i, layer in enumerate(layer_tags + [top_tags]):
        vertical_curves.append([gmsh.model.geo.addLine(previous_layer[j], layer[j]) for j in range(num_points)])
        horizontal_curves.append([gmsh.model.geo.addLine(layer[j], layer[(j + 1) % num_points]) for j in range(num_points)])
        previous_layer = layer

    gmsh.model.geo.addCurveLoop(base_curves, tag=500)
    gmsh.model.geo.addCurveLoop(orifice_curves, tag=400)
    gmsh.model.geo.addPlaneSurface([500, -400], tag=5)
    
    lateral_surfaces = []
    for i in range(num_layers):
        for j in range(num_points):
            curve_loop_tag = 600 + i * num_points + j
            plane_surface_tag = 700 + i * num_points + j
            
            if i == 0:
                layer_curves = [
                    vertical_curves[i][j],  # Línea vertical inferior a superior
                    horizontal_curves[i][j],  # Línea horizontal en la capa superior
                    -vertical_curves[i][(j + 1) % num_points],  # Línea vertical siguiente
                    -base_curves[j] # linea horizontal de la base
                ]
            else:
                layer_curves = [
                    vertical_curves[i][j],
                    horizontal_curves[i][j],
                    -vertical_curves[i][(j + 1) % num_points],
                    -horizontal_curves[i-1][j]
                ]

            gmsh.model.geo.addCurveLoop(layer_curves, tag=curve_loop_tag)
            gmsh.model.geo.addPlaneSurface([curve_loop_tag], tag=plane_surface_tag)
            lateral_surfaces.append(plane_surface_tag)
    
    gmsh.model.geo.addSurfaceLoop([5] + lateral_surfaces, tag=6)

    gmsh.model.geo.synchronize()
    gmsh.option.setNumber("Geometry.Tolerance", 1e-6)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 0.05)
    gmsh.model.mesh.generate(3)
    
    gmsh.write("Silo.stl")
    gmsh.finalize()


def generate_lid(orifice_width, orifice_height, num_points=4):
    gmsh.initialize()
    gmsh.model.add("Lid")


    # Orifice points
    orifice_points = []
    orifice_points.append((orifice_width / 2, -orifice_height / 2)) # h/2, -l/2
    orifice_points.append((orifice_width / 2, orifice_height / 2))  # h/2, l/2
    orifice_points.append((-orifice_width / 2, orifice_height / 2)) # -h/2, l/2
    orifice_points.append((-orifice_width / 2, -orifice_height / 2)) # -h/2, -l/2
    
    orifice_tags = []
    for i, (x, y) in enumerate(orifice_points):
        tag = 100 + i
        gmsh.model.geo.addPoint(x, y, 0, tag=tag)
        orifice_tags.append(tag)

    orifice_curves = [gmsh.model.geo.addLine(orifice_tags[i], orifice_tags[(i + 1) % num_points]) for i in range(num_points)]

    gmsh.model.geo.addCurveLoop([i + 1 for i in range(num_points)], tag=1)  # Orifice
    gmsh.model.geo.addPlaneSurface([1], tag=1)

    gmsh.model.geo.synchronize()
    gmsh.option.setNumber("Geometry.Tolerance", 1e-6)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 0.01)
    gmsh.model.mesh.generate(2)
    gmsh.write("Lid.stl")
    gmsh.finalize()


def generate_insertionsface(insertions_width, insertions_height, height, num_points=4):
    gmsh.initialize()
    gmsh.model.add("Insertionsface")


    # insertions_points
    insertions_points = []
    insertions_points.append((insertions_width / 2, -insertions_height / 2)) # h/2, -l/2
    insertions_points.append((insertions_width / 2, insertions_height / 2))  # h/2, l/2
    insertions_points.append((-insertions_width / 2, insertions_height / 2)) # -h/2, l/2
    insertions_points.append((-insertions_width / 2, -insertions_height / 2)) # -h/2, -l/2
    
    insertions_tags = []
    for i, (x, y) in enumerate(insertions_points):
        tag = 100 + i
        gmsh.model.geo.addPoint(x, y, height, tag=tag)
        insertions_tags.append(tag)

    insertions_curves = [gmsh.model.geo.addLine(insertions_tags[i], insertions_tags[(i + 1) % num_points]) for i in range(num_points)]

    gmsh.model.geo.addCurveLoop([i + 1 for i in range(num_points)], tag=1)
    gmsh.model.geo.addPlaneSurface([1], tag=1)

    gmsh.model.geo.synchronize()
    gmsh.option.setNumber("Geometry.Tolerance", 1e-6)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 0.01)    
    gmsh.model.mesh.generate(2)
    gmsh.write("Insertionsface.stl")
    gmsh.finalize()


def main():
    params = read_params("sim.params")
    
    orifice_diameter = params.get("Orifice_diameter")
    particle_diameter = params.get("Particle_diameter")

    
    generate_silo(orifice_diameter, 1.09*particle_diameter, 40.2*particle_diameter, 1.1*particle_diameter, 65.0*particle_diameter)
    generate_lid(orifice_diameter, 1.09*particle_diameter)
    generate_insertionsface(38*particle_diameter, 1.0*particle_diameter, 64.0*particle_diameter)


if __name__ == "__main__":
    main()
