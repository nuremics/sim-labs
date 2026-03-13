import json
from pathlib import Path


def label_entities(
    dim: int,
    infile: Path,
    outfile: str,
):
    """
    Label geometric entities on a CAD model and export the labeling information.

    Depending on the specified dimension, this function identifies
    key entities (constraints, loads, domain) on the geometry and
    stores their indices in a JSON file.

    Parameters
    ----------
    dim : int
        Dimension of the geometry model:
        - 1 for a 1D line (beam)
        - 2 for a 2D surface (shell)
        - 3 for a 3D volume (solid)
    infile : Path
        Path to the input CAD file.
    outfile : str
        Path to the output JSON file where the labeling information
        (entity indices for constraints, loads, and domain) will be saved.
    """

    # List of ids corresponding to each label is 
    # retrieved from the CAD automatic generation
    if dim == 3:
        ids_constraint = [1]
        ids_load = [2]
    
    elif dim == 2:
        ids_constraint = [4]
        ids_load = [2]
    
    elif dim == 1:
        ids_constraint = [1]
        ids_load = [2]
    
    # Define dictionary containing the labeled entities
    dict_labels = {
        "geometry": str(infile),
        "entities":{
            "Constraint": {
                "dim": dim-1,
                "ids": ids_constraint,
            },
            "Load": {
                "dim": dim-1,
                "ids": ids_load,
            },
            "Body": {
                "dim": dim,
                "ids": [1],
            },
        },
    }

    # Export the labeling information to a JSON file
    with open(outfile, "w") as f:
        json.dump(dict_labels, f, indent=4)