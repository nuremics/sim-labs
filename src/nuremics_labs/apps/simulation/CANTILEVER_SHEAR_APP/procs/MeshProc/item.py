import os
import attrs
import json
from pathlib import Path

from nuremics import Process
from nuremics_labs.apps.simulation.CANTILEVER_SHEAR_APP.procs.MeshProc.ops import (
    generate_mesh,
)


@attrs.define
class MeshProc(Process):
    """
    Discretize the geometric representation of a physical system 
    into a computational mesh.

    Process
    -------
        A/ generate_mesh
            Generate and export a computational mesh from a geometric model 
            by discretizing the domain into mesh entities (nodes, elements)
            and assigning labeled physical groups.

    Input parameters
    ----------------
        dim : int
            Dimension of the geometry: 
            - 1 for a 1D line
            - 2 for a 2D surface
            - 3 for a 3D volume

    Input paths
    -----------
        infile : json
            File containing the geometric model and associated labels.
        mesh_settings_file : json
            File containing the mesh discretization settings.

    Outputs
    -------
        outfile : msh
            File containing the computational mesh (exported in Gmsh format).
    """

    # Parameters
    dim: int = attrs.field(init=False, metadata={"input": True})

    # Paths
    infile: Path = attrs.field(init=False, metadata={"input": True}, converter=Path)
    mesh_settings_file: Path = attrs.field(init=False, metadata={"input": True}, converter=Path)

    # Outputs
    outfile: Path = attrs.field(init=False, metadata={"output": True}, converter=Path)

    def __call__(self):
        super().__call__()

        self.generate_mesh()

    def generate_mesh(self):
        """
        Generate and export a computational mesh from a geometric model 
        by discretizing the domain into mesh entities (nodes, elements)
        and assigning labeled physical groups.

        Uses
        ----
            dim
            infile
            mesh_settings_file
        
        Generates
        ---------
            outfile
        """

        # Load mesh settings
        with open(self.mesh_settings_file) as f:
            dict_mesh_settings = json.load(f)

        generate_mesh(
            infile=str(self.infile),
            outfile=str(self.outfile),
            dim=self.dim,
            elem=dict_mesh_settings["elem"],
            nb_elem_length=dict_mesh_settings["nb_elem_length"],
            nb_elem_width=dict_mesh_settings["nb_elem_width"],
            nb_elem_height=dict_mesh_settings["nb_elem_height"],
        )


if __name__ == "__main__":

    # ================================================================== #
    #                      USER-DEFINED PARAMETERS                       #
    #              >>>>> TO BE EDITED BY THE OPERATOR <<<<<              #
    # ================================================================== #

    # Working directory
    working_dir = Path(r"...")

    # Input parameters
    dim = 3

    # Input paths
    infile = Path(r"...")
    mesh_settings_file = Path(r"...")

    # Output paths
    outfile = "mesh.msh"

    # ================================================================== #

    # Go to working directory
    os.chdir(working_dir)

    # Create dictionary containing input data
    dict_inputs = {
        "dim": dim,
        "infile": infile,
        "mesh_settings_file": mesh_settings_file,
        "outfile": outfile,
    }

    # Create process
    process = MeshProc(
        dict_inputs=dict_inputs,
        set_inputs=True,
    )

    # Run process
    process()
    process.finalize()