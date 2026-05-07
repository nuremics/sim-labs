import re

import numpy as np
import pyvista as pv


def build_model(
    infile: str,
    outfile: str,
) -> None:

    # Get physical groups from mesh
    dict_physical_groups = _get_gmsh_physical_groups(
        infile=infile,
    )

    # Read mesh
    mesh: pv.UnstructuredGrid = pv.read(infile)

    # Define point data to tag nodes on which boundary conditions should be applied
    mesh.point_data["Inlet"] = np.zeros((mesh.n_points), dtype=int)
    _tag_boundary_conditions_nodes(
        ugrid=mesh,
        dict_physical_groups=dict_physical_groups,
        group="Inlet",
        bc_name="Inlet",
    )
    mesh.point_data["Outlet"] = np.zeros((mesh.n_points), dtype=int)
    _tag_boundary_conditions_nodes(
        ugrid=mesh,
        dict_physical_groups=dict_physical_groups,
        group="Outlet",
        bc_name="Outlet",
    )
    mesh.point_data["Walls"] = np.zeros((mesh.n_points), dtype=int)
    _tag_boundary_conditions_nodes(
        ugrid=mesh,
        dict_physical_groups=dict_physical_groups,
        group="Walls",
        bc_name="Walls",
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
            id_init = i + 2
            nb_physical_groups = int(lines[i + 1])
            break
    
    dict_physical_groups = {}
    for i in range(nb_physical_groups):
        list_line = lines[id_init + i].split(" ")
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
    ids = np.where(mask)[0].tolist()
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