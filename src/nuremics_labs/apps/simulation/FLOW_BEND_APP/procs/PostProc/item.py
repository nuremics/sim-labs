import os
from pathlib import Path

import attrs
import pandas as pd
from nuremics import Process

from nuremics_labs.apps.simulation.FLOW_BEND_APP.procs.PostProc.ops import (
    get_probes_velocity,
    plot_probes_velocity,
)


@attrs.define
class PostProc(Process):

    # Parameters
    r: float = attrs.field(init=False, metadata={"input": True})

    # Paths
    solution_dir: Path = attrs.field(init=False, metadata={"input": True}, converter=Path)

    # Outputs
    data_file: Path = attrs.field(init=False, metadata={"output": True}, converter=Path)
    fig_file: Path = attrs.field(init=False, metadata={"output": True}, converter=Path)

    # Internal
    df_probes: pd.DataFrame = attrs.field(init=False)

    def __call__(self) -> None:
        super().__call__()

        self.get_probes_velocity()
        self.plot_probes_velocity()

    def get_probes_velocity(self) -> None:

        self.df_probes = get_probes_velocity(
            r=self.r,
            solution_dir=self.solution_dir,
            data_file=self.data_file,
        )

    def plot_probes_velocity(self) -> None:

        plot_probes_velocity(
            df=self.df_probes,
            fig_file=str(self.fig_file),
        )


if __name__ == "__main__":

    # ================================================================== #
    #                      USER-DEFINED PARAMETERS                       #
    #              >>>>> TO BE EDITED BY THE OPERATOR <<<<<              #
    # ================================================================== #

    # Working directory
    working_dir = Path(r"C:\Users\julie\Documents\nuRemics\test")

    # Input parameters
    r = 2.0

    # Input paths
    solution_dir = Path(r"C:\Users\julie\Documents\nuRemics\test\solution")

    # Output paths
    data_file = "probes.csv"
    fig_file = "probes.png"

    # ================================================================== #

    # Go to working directory
    os.chdir(working_dir)

    # Create dictionary containing input data
    dict_inputs = {
        "r": r,
        "solution_dir": solution_dir,
        "data_file": data_file,
        "fig_file": fig_file,
    }

    # Create process
    process = PostProc(
        dict_inputs=dict_inputs,
        set_inputs=True,
    )

    # Run process
    process()
    process.finalize()