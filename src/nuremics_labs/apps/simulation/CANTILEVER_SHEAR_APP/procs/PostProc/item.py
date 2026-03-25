import os
import attrs
from pathlib import Path

import pandas as pd

from nuremics import Process
from nuremics_labs.apps.simulation.CANTILEVER_SHEAR_APP.procs.PostProc.ops import (
   get_deflection,
   plot_deflection,
)


@attrs.define
class PostProc(Process):
    """
    Post-process simulation results to extract relevant metrics.

    Process
    -------
        A/ get_deflection
            Extract the displacement at the extremity of the object from raw 
            simulation results and save it to a metric data file.
        B/ plot_deflection
            Plot the displacement metric over time.

    Input parameters
    ----------------
        NA

    Input paths
    -----------
        model_file : vtk
            File containing the model object.
        solution_dir : folder
            Directory containing the simulation results.

    Outputs
    -------
        data_file : xlsx
            File containing the computed displacement metric.
        fig_file : png
            File containing the visual representation of the displacement metric.
    """

    # Paths
    model_file: Path = attrs.field(init=False, metadata={"input": True}, converter=Path)
    solution_dir: Path = attrs.field(init=False, metadata={"input": True}, converter=Path)

    # Outputs
    data_file: Path = attrs.field(init=False, metadata={"output": True}, converter=Path)
    fig_file: Path = attrs.field(init=False, metadata={"output": True}, converter=Path)

    # Internal
    df_metrics: pd.DataFrame = attrs.field(init=False)

    def __call__(self):
        super().__call__()

        self.get_deflection()
        self.plot_deflection()

    def get_deflection(self):
        """
        Extract the displacement at the extremity of the object from raw 
        simulation results and save it to a metric data file.

        Uses
        ----
            model_file
            solution_dir
        
        Generates
        ---------
            df_metrics
            data_file
        """

        self.df_metrics = get_deflection(
            model_file=str(self.model_file),
            solution_dir=self.solution_dir,
            data_file=self.data_file,
        )

    def plot_deflection(self):
        """
        Plot the displacement metric over time.

        Uses
        ----
            df_metrics
        
        Generates
        ---------
            fig_file
        """

        plot_deflection(
            df=self.df_metrics,
            fig_file=str(self.fig_file),
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
    model_file = Path(r"...")
    solution_dir = Path(r"...")

    # Output paths
    data_file = "metrics.xlsx"
    fig_file = "deflection.png"

    # ================================================================== #

    # Go to working directory
    os.chdir(working_dir)

    # Create dictionary containing input data
    dict_inputs = {
        "model_file": model_file,
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