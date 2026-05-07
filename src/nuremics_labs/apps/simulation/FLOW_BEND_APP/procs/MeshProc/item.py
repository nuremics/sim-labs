import json
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
    # mesh_settings_file: Path = attrs.field(init=False, metadata={"input": True}, converter=Path)

    # Outputs
    outfile: Path = attrs.field(init=False, metadata={"output": True}, converter=Path)

    def __call__(self) -> None:
        super().__call__()

        self.generate_mesh()

    def generate_mesh(self) -> None:

        # with open(self.mesh_settings_file) as f:
        #     dict_mesh_settings = json.load(f)

        generate_mesh(
            dx=self.dx,
            infile=str(self.infile),
            outfile=str(self.outfile),
            # dim=self.dim,
            # elem=dict_mesh_settings["elem"],
            # nb_elem_length=dict_mesh_settings["nb_elem_length"],
            # nb_elem_width=dict_mesh_settings["nb_elem_width"],
            # nb_elem_height=dict_mesh_settings["nb_elem_height"],
        )


if __name__ == "__main__":

    # ================================================================== #
    #                      USER-DEFINED PARAMETERS                       #
    #              >>>>> TO BE EDITED BY THE OPERATOR <<<<<              #
    # ================================================================== #

    # Working directory
    working_dir = Path(r"C:\Users\julie\Documents\nuRemics\test")

    # Input parameters
    dx = 0.5

    # Input paths
    infile = Path(r"C:\Users\julie\Documents\nuRemics\test") / "labels.json"
    # mesh_settings_file = Path(r"...")

    # Output paths
    outfile = "mesh.msh"

    # ================================================================== #

    # Go to working directory
    os.chdir(working_dir)

    # Create dictionary containing input data
    dict_inputs = {
        "dx": dx,
        "infile": infile,
        # "mesh_settings_file": mesh_settings_file,
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