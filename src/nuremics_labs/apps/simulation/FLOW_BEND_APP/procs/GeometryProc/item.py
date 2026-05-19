import os
from pathlib import Path

import attrs
from nuremics import Process

from nuremics_labs.apps.simulation.FLOW_BEND_APP.procs.GeometryProc.ops import (
    create_geometry,
)


@attrs.define
class GeometryProc(Process):

    # Parameters
    r: float = attrs.field(init=False, metadata={"input": True})
    R: float = attrs.field(init=False, metadata={"input": True})
    L0: float = attrs.field(init=False, metadata={"input": True})
    L1: float = attrs.field(init=False, metadata={"input": True})

    # Outputs
    outfile: Path = attrs.field(init=False, metadata={"output": True}, converter=Path)

    def __call__(self) -> None:
        super().__call__()

        self.create_geometry()

    def create_geometry(self) -> None:

        create_geometry(
            r=self.r,
            R=self.R,
            L0=self.L0,
            L1=self.L1,
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
    r=2.0
    R=5.0
    L0=20.0
    L1=10.0

    # Output paths
    outfile = "geometry.brep"

    # ================================================================== #

    # Go to working directory
    os.chdir(working_dir)

    # Create dictionary containing input data
    dict_inputs = {
        "r": r,
        "R": R,
        "L0": L0,
        "L1": L1,
        "outfile": outfile,
    }

    # Create process
    process = GeometryProc(
        dict_inputs=dict_inputs,
        set_inputs=True,
    )

    # Run process
    process()
    process.finalize()