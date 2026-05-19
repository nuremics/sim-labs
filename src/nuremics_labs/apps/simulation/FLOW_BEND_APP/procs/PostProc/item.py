import os
from pathlib import Path

import attrs
import pandas as pd
from nuremics import Process

from nuremics_labs.apps.simulation.FLOW_BEND_APP.procs.PostProc.ops import (
    get_probes_velocity,
    plot_probes_velocity,
    get_velocity_profiles,
    plot_velocity_profiles,
)


@attrs.define
class PostProc(Process):

    # Parameters
    r: float = attrs.field(init=False, metadata={"input": True})
    R: float = attrs.field(init=False, metadata={"input": True})

    # Paths
    solution_dir: Path = attrs.field(init=False, metadata={"input": True}, converter=Path)

    # Outputs
    probes_data_file: Path = attrs.field(init=False, metadata={"output": True}, converter=Path)
    probes_fig_file: Path = attrs.field(init=False, metadata={"output": True}, converter=Path)
    profiles_data_file: Path = attrs.field(init=False, metadata={"output": True}, converter=Path)
    profiles_fig_file: Path = attrs.field(init=False, metadata={"output": True}, converter=Path)

    # Internal
    df_probes: pd.DataFrame = attrs.field(init=False)
    df_profiles: pd.DataFrame = attrs.field(init=False)

    def __call__(self) -> None:
        super().__call__()

        self.get_probes_velocity()
        self.plot_probes_velocity()
        self.get_velocity_profiles()
        self.plot_velocity_profiles()

    def get_probes_velocity(self) -> None:

        self.df_probes = get_probes_velocity(
            r=self.r,
            solution_dir=self.solution_dir,
            data_file=self.probes_data_file,
        )

    def plot_probes_velocity(self) -> None:

        plot_probes_velocity(
            df=self.df_probes,
            fig_file=str(self.probes_fig_file),
        )

    def get_velocity_profiles(self) -> None:

        self.df_profiles = get_velocity_profiles(
            r=self.r,
            R=self.R,
            solution_dir=self.solution_dir,
            data_file=self.profiles_data_file,
        )

    def plot_velocity_profiles(self) -> None:

        plot_velocity_profiles(
            df=self.df_profiles,
            fig_file=str(self.profiles_fig_file),
        )


if __name__ == "__main__":

    # ================================================================== #
    #                      USER-DEFINED PARAMETERS                       #
    #              >>>>> TO BE EDITED BY THE OPERATOR <<<<<              #
    # ================================================================== #

    # Working directory
    working_dir = Path(r"...")

    # Input parameters
    r = 2.0
    R = 5.0

    # Input paths
    solution_dir = Path(r"...") / "solution"

    # Output paths
    probes_data_file = "probes.csv"
    probes_fig_file = "probes.png"
    profiles_data_file = "profiles.csv"
    profiles_fig_file = "profiles.png"

    # ================================================================== #

    # Go to working directory
    os.chdir(working_dir)

    # Create dictionary containing input data
    dict_inputs = {
        "r": r,
        "R": R,
        "solution_dir": solution_dir,
        "probes_data_file": probes_data_file,
        "probes_fig_file": probes_fig_file,
        "profiles_data_file": profiles_data_file,
        "profiles_fig_file": profiles_fig_file,
    }

    # Create process
    process = PostProc(
        dict_inputs=dict_inputs,
        set_inputs=True,
    )

    # Run process
    process()
    process.finalize()