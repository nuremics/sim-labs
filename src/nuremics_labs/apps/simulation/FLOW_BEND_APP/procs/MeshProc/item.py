import os
from pathlib import Path

import attrs
from nuremics import Process

from nuremics_labs.apps.simulation.FLOW_BEND_APP.procs.MeshProc.ops import (
    generate_mesh,
)


@attrs.define
class MeshProc(Process):

    # Parameters
    dx: float = attrs.field(init=False, metadata={"input": True})

    # Paths
    infile: Path = attrs.field(init=False, metadata={"input": True}, converter=Path)

    # Outputs
    outfile: Path = attrs.field(init=False, metadata={"output": True}, converter=Path)

    def __call__(self) -> None:
        super().__call__()

        self.generate_mesh()

    def generate_mesh(self) -> None:

        generate_mesh(
            dx=self.dx,
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
    dx = 0.5

    # Input paths
    infile = Path(r"...") / "labels.json"

    # Output paths
    outfile = "mesh.msh"

    # ================================================================== #

    # Go to working directory
    os.chdir(working_dir)

    # Create dictionary containing input data
    dict_inputs = {
        "dx": dx,
        "infile": infile,
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