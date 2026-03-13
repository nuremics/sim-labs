from typing import Optional

from nuremics import Application

from nuremics_labs.apps.simulation.CANTILEVER_SHEAR_APP.procs import GeometryProc
from nuremics_labs.apps.simulation.CANTILEVER_SHEAR_APP.procs import LabelingProc

APP_NAME = "CANTILEVER_SHEAR_APP"


def main(
    stage: Optional[str] = "run",
) -> None:

    # --------------- #
    # Define workflow #
    # --------------- #
    workflow = [
        {
            "process": GeometryProc,
            "user_params": {
                "dim": "dimension",
            },
            "hard_params": {
                "length": 10.0,
                "width": 1.0,
                "height": 0.1,
            },
            "output_paths": {
                "outfile": "geometry.brep",
            },
        },
        {
            "process": LabelingProc,
            "user_params": {
                "dim": "dimension",
            },
            "required_paths": {
                "infile": "geometry.brep",
            },
            "output_paths": {
                "outfile": "labels.json",
            },
        },
    ]

    # ----------------------------------- #
    # Define default values of parameters #
    # ----------------------------------- #
    default_params = {
        "dimension": 3,
    }

    # ------------------ #
    # Define application #
    # ------------------ #
    app = Application(
        app_name=APP_NAME,
        workflow=workflow,
    )
    if stage == "config":
        app.configure()
    elif stage == "settings":
        app.configure()
        app.settings()
    elif stage == "run":
        app.configure()
        app.settings()
        app()
    
    return workflow, app, default_params


if __name__ == "__main__":

    # --------------- #
    # Run application #
    # --------------- #
    main()