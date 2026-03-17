import json
import gmsh


def generate_mesh(
    infile: str,
    outfile: str,
    dim: int,
    elem: str,
    nb_elem_length: int = None,
    nb_elem_width: int = None,
    nb_elem_height: int = None,
) -> None:
    """
    Generate and export a computational mesh from a geometric model 
    by discretizing the domain into mesh entities (nodes, elements)
    and assigning labeled physical groups.

    Parameters
    ----------
    infile : str
        Path to the file containing the geometric model 
        and associated labels (JSON format).
    outfile : str
        Path to the output mesh file. The mesh is exported in Gmsh
        format (.msh).
    dim : int
        Dimension of the geometry: 
        - 1 for a 1D line
        - 2 for a 2D rectangle
        - 3 for a 3D box
    elem : str
        Type of finite elements to generate ("hexa" or "tetra").
    nb_elem_length : int
        Number of elements along the X axis (length direction).
    nb_elem_width : int
        Number of elements along the Y axis (width direction),
        required if dim = 2 or 3.
    nb_elem_height : int
        Number of elements along the Z axis (height direction),
        required if dim = 3.
    """

    # Read file containing geometry path and labels
    with open(infile) as f:
        dict_labels = json.load(f)

    # Initialize gmsh
    gmsh.initialize(
        interruptible=False
    )
    gmsh.clear()

    # Open geometry file
    gmsh.open(dict_labels["geometry"])

    # Synchronize gmsh
    gmsh.model.occ.synchronize()

    # Add physical groups on each label
    for label, value in dict_labels["entities"].items():
        gmsh.model.addPhysicalGroup(
            dim=value["dim"],
            tags=value["ids"],
            name=label,
        )
    
    # Synchronize gmsh
    gmsh.model.occ.synchronize()

    # Define discretization
    num_nodes_length = nb_elem_length+1
    if dim > 1:
        num_nodes_width = nb_elem_width+1
    if dim == 3:
        num_nodes_height = nb_elem_height+1

    # Define mesh
    if dim == 3:

        for tag in [9, 10, 11, 12]:
            gmsh.model.mesh.setTransfiniteCurve(
                tag=tag,
                numNodes=num_nodes_length,
            )
        for tag in [2, 4, 6, 8]:
            gmsh.model.mesh.setTransfiniteCurve(
                tag=tag,
                numNodes=num_nodes_width,
            )
        for tag in [1, 3, 5, 7]:
            gmsh.model.mesh.setTransfiniteCurve(
                tag=tag,
                numNodes=num_nodes_height,
            )
        for tag in [1, 2, 3, 4, 5, 6]:
            gmsh.model.mesh.setTransfiniteSurface(
                tag=tag,
            )
            if (elem == "hexa"):
                gmsh.model.mesh.setRecombine(
                    dim=2,
                    tag=tag,
                )
        gmsh.model.mesh.setTransfiniteVolume(
            tag=1,
        )
        if (elem == "hexa"):
            gmsh.model.mesh.recombine()
    
    # Generate mesh
    gmsh.model.mesh.generate(dim)

    # Optimize mesh
    gmsh.model.mesh.optimize("Netgen")

    # Save mesh file
    gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)
    gmsh.write(outfile)
    
    # Finalize gmsh
    gmsh.clear()
    gmsh.finalize()