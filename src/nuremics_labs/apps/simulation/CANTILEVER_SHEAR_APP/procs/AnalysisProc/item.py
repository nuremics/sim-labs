import json
import os
from pathlib import Path

import attrs
from nuremics import Process

from nuremics_labs.apps.simulation.CANTILEVER_SHEAR_APP.procs.AnalysisProc.ops import (
    plot_overall,
    summarize_overall_errors,
)


@attrs.define
class AnalysisProc(Process):
    """
    Analyze the results of multiple simulation runs to identify trends, compare metrics,
    and draw conclusions.

    Pipeline
    --------
        A/ plot_overall
            Visualize and compare the metrics of the various simulation runs on a single plot.
        B/ summarize_overall_errors
            Compile and summarize the deviations between computed simulation results and 
            reference solutions for all performed tests.

    Analysis
    --------
        data_file : xlsx
            File containing the computed displacement metric.

    Outputs
    -------
        fig_file : png
            File containing the visual comparisons of the metrics for the various
            simulation runs.
        error_file : csv
            File summarizing the obtained errors across all simulation runs.
    """

    # Analysis
    metadata = {
        "input": True,
        "analysis": True,
    }
    data_file: str = attrs.field(init=False, metadata=metadata)

    # Outputs
    fig_file: Path = attrs.field(init=False, metadata={"output": True}, converter=Path)
    error_file: Path = attrs.field(init=False, metadata={"output": True}, converter=Path)

    def __call__(self) -> None:
        super().__call__()

        self.plot_overall()
        self.summarize_overall_errors()
    
    def plot_overall(self) -> None:
        """
        Visualize and compare the metrics of the various simulation runs on a single plot.

        Uses
        ----
            data_file

        Generates
        ---------
            fig_file
        """

        self.process_output(
            out=self.data_file,
            func=plot_overall,
            filename=self.fig_file,
        )
    
    def summarize_overall_errors(self) -> None:
        """
        Compile and summarize the deviations between computed simulation results and 
        reference solutions for all performed tests.

        Uses
        ----
            data_file

        Generates
        ---------
            error_file
        """

        self.process_output(
            out=self.data_file,
            func=summarize_overall_errors,
            filename=self.error_file,
        )


if __name__ == "__main__":

    # ================================================================== #
    #                      USER-DEFINED PARAMETERS                       #
    #              >>>>> TO BE EDITED BY THE OPERATOR <<<<<              #
    # ================================================================== #
    
    # Define working directory
    working_dir = Path(r"...")

    # Analysis
    data_file = "metrics.xlsx"

    # Output paths
    fig_file = "overall_comparisons.png"
    error_file = "overall_errors.csv"

    # Paths file
    paths_file = working_dir.parents[0] / ".paths.json"

    # Analysis file
    analysis_file = working_dir.parents[0] / "analysis.json"

    # ================================================================== #

    # Go to working directory
    os.chdir(working_dir)

    # Create dictionary containing input data
    dict_inputs = {
        "data_file": data_file,
        "fig_file": fig_file,
        "error_file": error_file,
    }
    
    # Create process
    process = AnalysisProc(
        dict_inputs=dict_inputs,
        set_inputs=True,
    )
    process.name = process.__class__.__name__
    process.is_case = False

    # Get dictionary of paths
    with open(paths_file) as f:
        process.dict_paths = json.load(f)

    # Get dictionary of analysis settings
    with open(analysis_file) as f:
        process.dict_analysis = json.load(f) 

    # Run process
    process()
    process.finalize()