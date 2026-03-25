import os
from pathlib import Path

import attrs
from nuremics import Process

from nuremics_labs.apps.simulation.CANTILEVER_SHEAR_APP.procs.ModelProc.ops import (
    build_model,
)


@attrs.define
class ModelProc(Process):
    """
    Convert a meshed geometry into a model object mapping geometric labels
    to mesh entities.

    Process
    -------
        A/ build_model
            Build a VTK-based model object from a meshed geometry by creating
            data fields that map physical groups to their corresponding 
            nodes and elements.

    Input parameters
    ----------------
        NA

    Input paths
    -----------
        infile : msh
            File containing the meshed geometry and physical group definitions
            (in Gmsh format).

    Outputs
    -------
        outfile : vtk
            File containing the model object.
    """

    # Paths
    infile: Path = attrs.field(init=False, metadata={"input": True}, converter=Path)

    # Outputs
    outfile: Path = attrs.field(init=False, metadata={"output": True}, converter=Path)

    def __call__(self) -> None:
        super().__call__()

        self.build_model()

    def build_model(self) -> None:
        """
        Build a VTK-based model object from a meshed geometry by creating
        data fields that map physical groups to their corresponding 
        nodes and elements.

        Uses
        ----
            infile
        
        Generates
        ---------
            outfile
        """

        build_model(
            infile=str(self.infile),
            outfile=str(self.outfile),
        )


if __name__ == "__main__":

    # ================================================================== #
    #                      USER-DEFINED PARAMETERS                       #
    #              >>>>> TO BE EDITED BY THE OPERATOR <<<<<              #
    # ================================================================== #

    # Working directory
    working_dir = Path(r"...")

    # Input parameters
    # NA

    # Input paths
    infile = Path(r"...")

    # Output paths
    outfile = "model.vtk"

    # ================================================================== #

    # Go to working directory
    os.chdir(working_dir)

    # Create dictionary containing input data
    dict_inputs = {
        "infile": infile,
        "outfile": outfile,
    }

    # Create process
    process = ModelProc(
        dict_inputs=dict_inputs,
        set_inputs=True,
    )

    # Run process
    process()
    process.finalize()