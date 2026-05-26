from pathlib import Path

import attrs
from nuremics import Process

from nuremics_labs.apps.simulation.FLOW_BEND_APP.procs.AnalysisProc.ops import (
    plot_overall,
)


@attrs.define
class AnalysisProc(Process):

    # Analysis
    metadata = {
        "input": True,
        "analysis": True,
    }
    data_file: str = attrs.field(init=False, metadata=metadata)

    # Outputs
    fig_file: Path = attrs.field(init=False, metadata={"output": True}, converter=Path)

    def __call__(self) -> None:
        super().__call__()

        self.plot_overall()
    
    def plot_overall(self) -> None:

        self.process_output(
            out=self.data_file,
            func=plot_overall,
            filename=self.fig_file,
        )


if __name__ == "__main__":

    import json
    import os

    # ================================================================== #
    #                      USER-DEFINED PARAMETERS                       #
    #              >>>>> TO BE EDITED BY THE OPERATOR <<<<<              #
    # ================================================================== #
    
    # Define working directory
    working_dir = Path(r"...")

    # Analysis
    data_file = "profiles.csv"

    # Output paths
    fig_file = "overall_comparisons.png"

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