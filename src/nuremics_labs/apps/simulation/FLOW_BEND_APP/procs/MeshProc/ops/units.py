import json

import gmsh


def generate_mesh(
    dx: float,
    infile: str,
    outfile: str,
) -> None:

    with open(infile) as f:
        dict_labels = json.load(f)

    gmsh.initialize(
        interruptible=False
    )
    gmsh.clear()

    gmsh.open(dict_labels["geometry"])
    gmsh.model.occ.synchronize()

    for label, value in dict_labels["entities"].items():
        
        gmsh.model.addPhysicalGroup(
            dim=value["dim"],
            tags=value["ids"],
            tag=value["marker"],
        )
        gmsh.model.setPhysicalName(
            dim=value["dim"],
            tag=value["marker"],
            name=label,
        )
    
    gmsh.model.occ.synchronize()

    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 0.5*dx)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", dx)
    gmsh.model.mesh.generate(3)
    gmsh.model.mesh.optimize("Netgen")
    gmsh.model.mesh.setOrder(2)

    gmsh.write(outfile)
    
    gmsh.clear()
    gmsh.finalize()