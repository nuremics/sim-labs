import os
import attrs
import json
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
    model_file: Path = attrs.field(init=False, metadata={"input": True}, converter=Path)
    solution_dir: Path = attrs.field(init=False, metadata={"input": True}, converter=Path)

    # Outputs
    data_file: Path = attrs.field(init=False, metadata={"output": True}, converter=Path)
    fig_file: Path = attrs.field(init=False, metadata={"output": True}, converter=Path)

    # Internal
    df_results: pd.DataFrame = attrs.field(init=False)

    def __call__(self):
        super().__call__()

        self.get_deflection()
        self.plot_deflection()

    def get_deflection(self):
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

        self.df_results = get_deflection(
            model_file=str(self.model_file),
            solution_dir=self.solution_dir,
            data_file=self.data_file,
        )

    def plot_deflection(self):
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

        plot_deflection(
            df=self.df_results,
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