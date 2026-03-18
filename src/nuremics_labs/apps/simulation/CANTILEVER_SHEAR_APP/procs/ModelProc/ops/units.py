import re

import pyvista as pv
import numpy as np


def build_model(
    infile: str,
    outfile: str,
) -> None:
    """
    Build a VTK-based model object from a meshed geometry by creating
    data fields that map physical groups to their corresponding nodes 
    and elements.

    Parameters
    ----------
    infile : str
        Path to the mesh file (in Gmsh format) containing the meshed 
        geometry and physical group definitions.
    outfile : str
        Path to the model object (exported in VTK format).
    """

    # Get physical groups from mesh
    dict_physical_groups = _get_gmsh_physical_groups(
        infile=infile,
    )

    # Read mesh
    mesh: pv.UnstructuredGrid = pv.read(infile)

    # Define point data to tag nodes on which boundary conditions should be applied
    mesh.point_data["Constraint"] = np.zeros((mesh.n_points), dtype=int)
    _tag_boundary_conditions_nodes(
        ugrid=mesh,
        dict_physical_groups=dict_physical_groups,
        group="Constraint",
        bc_name="Constraint",
    )
    mesh.point_data["Load"] = np.zeros((mesh.n_points), dtype=int)
    _tag_boundary_conditions_nodes(
        ugrid=mesh,
        dict_physical_groups=dict_physical_groups,
        group="Load",
        bc_name="Load",
    )

    # Write model file
    mesh.save(
        filename=outfile,
        binary=False,
    )


def _get_gmsh_physical_groups(
    infile: str,
) -> dict:
    
    f = open(
        file=infile,
        mode="r",
    )
    lines = f.readlines()

    for i, line in enumerate(lines):
        if "$PhysicalNames" in line:
            id_init = i+2
            nb_physical_groups = int(lines[i+1])
            break
    
    dict_physical_groups = {}
    for i in range(nb_physical_groups):
        list_line = lines[id_init+i].split(" ")
        match = re.search(r'"(.*?)"', list_line[2])
        key = match.group(1)
        dict_physical_groups[key] = [int(list_line[0]), int(list_line[1])]
    
    return dict_physical_groups


def _tag_boundary_conditions_nodes(
    ugrid: pv.UnstructuredGrid,
    dict_physical_groups: dict,
    group: str,
    bc_name: str,
) -> None:
    
    mask = ugrid.cell_data["gmsh:physical"] == dict_physical_groups[group][1]
    ids = np.where(mask == True)[0].tolist()
    for i in ids:
        for j in ugrid.get_cell(i).point_ids:
            if dict_physical_groups[group][0] == 0:
                for k in range(ugrid.n_points):
                    dist = np.linalg.norm(ugrid.points[k, :] - ugrid.points[j, :])
                    if dist < 1.0e-6:
                        ugrid.point_data[bc_name][k] = 1
                ugrid.point_data[bc_name][j] = 0
            else:
                ugrid.point_data[bc_name][j] = 1