import json

import gmsh
import numpy as np


def label_entities(
    R: float,
    L0: float,
    L1: float,
    infile: str,
    outfile: str,
) -> None:
    
    dict_labels = {
        "geometry": infile,
        "entities": {},
    }
    
    gmsh.initialize(
        interruptible=False,
    )
    gmsh.clear()

    gmsh.open(infile)
    gmsh.model.occ.synchronize()

    volumes = gmsh.model.getEntities(dim=3)

    dict_labels["entities"]["Fluid"] = {
        "dim": volumes[0][0],
        "ids": [volumes[0][1]],
        "marker": 1,
    }

    inlet, outlet, walls = [], [], []
    boundaries = gmsh.model.getBoundary(volumes, oriented=False)
    for boundary in boundaries:
        center_of_mass = gmsh.model.occ.getCenterOfMass(boundary[0], boundary[1])
        if np.allclose(center_of_mass, [R + L0, 0, R]):
            inlet.append(boundary[1])
        elif np.allclose(center_of_mass, [0, 0, -L1]):
            outlet.append(boundary[1])
        else:
            walls.append(boundary[1])

    dict_labels["entities"]["Inlet"] = {
        "dim": 2,
        "ids": inlet,
        "marker": 2,
    }
    dict_labels["entities"]["Outlet"] = {
        "dim": 2,
        "ids": outlet,
        "marker": 3,
    }
    dict_labels["entities"]["Walls"] = {
        "dim": 2,
        "ids": walls,
        "marker": 4,
    }

    with open(outfile, "w") as f:
        json.dump(dict_labels, f, indent=4)