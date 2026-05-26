import os
from pathlib import Path

import attrs
from nuremics import Process

from nuremics_labs.apps.simulation.FLOW_BEND_APP.procs.LabelingProc.ops import (
    label_entities,
)


@attrs.define
class LabelingProc(Process):

    # Parameters
    R: float = attrs.field(init=False, metadata={"input": True})
    L0: float = attrs.field(init=False, metadata={"input": True})
    L1: float = attrs.field(init=False, metadata={"input": True})

    # Paths
    infile: Path = attrs.field(init=False, metadata={"input": True}, converter=Path)

    # Outputs
    outfile: Path = attrs.field(init=False, metadata={"output": True}, converter=Path)

    def __call__(self) -> None:
        super().__call__()

        self.label_entities()

    def label_entities(self) -> None:
        
        label_entities(
            R=self.R,
            L0=self.L0,
            L1=self.L1,
            infile=str(self.infile),
            outfile=self.outfile,
        )


if __name__ == "__main__":

    # ================================================================== #
    #                      USER-DEFINED PARAMETERS                       #
    #              >>>>> TO BE EDITED BY THE OPERATOR <<<<<              #
    # ================================================================== #

    # Working directory
    working_dir = Path(r"...")

    # Input parameters
    R = 5.0
    L0 = 20.0
    L1 = 10.0

    # Input paths
    infile = Path(r"...") / "geometry.brep"

    # Output paths
    outfile = "labels.json"

    # ================================================================== #

    # Go to working directory
    os.chdir(working_dir)

    # Create dictionary containing input data
    dict_inputs = {
        "R": R,
        "L0": L0,
        "L1": L1,
        "infile": infile,
        "outfile": outfile,
    }

    # Create process
    process = LabelingProc(
        dict_inputs=dict_inputs,
        set_inputs=True,
    )

    # Run process
    process()
    process.finalize()