import os
from pathlib import Path

import attrs
from nuremics import Process

from nuremics_labs.apps.simulation.FLOW_BEND_APP.procs.ModelProc.ops import (
    build_model,
)


@attrs.define
class ModelProc(Process):

    # Paths
    infile: Path = attrs.field(init=False, metadata={"input": True}, converter=Path)

    # Outputs
    outfile: Path = attrs.field(init=False, metadata={"output": True}, converter=Path)

    def __call__(self) -> None:
        super().__call__()

        self.build_model()

    def build_model(self) -> None:

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
    infile = Path(r"...") / "mesh.msh"

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