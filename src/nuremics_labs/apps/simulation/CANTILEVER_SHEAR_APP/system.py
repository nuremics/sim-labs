from typing import Optional

from nuremics import Application

from nuremics_labs.apps.simulation.CANTILEVER_SHEAR_APP.procs import (
    AnalysisProc,
    GeometryProc,
    LabelingProc,
    MeshProc,
    ModelProc,
    PostProc,
    SolverProc,
)

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
            "hard_params": {
                "dim": 3,
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
            "hard_params": {
                "dim": 3,
            },
            "required_paths": {
                "infile": "geometry.brep",
            },
            "output_paths": {
                "outfile": "labels.json",
            },
        },
        {
            "process": MeshProc,
            "hard_params": {
                "dim": 3,
            },
            "user_paths": {
                "mesh_settings_file": "mesh_settings.json",
            },
            "required_paths": {
                "infile": "labels.json",
            },
            "output_paths": {
                "outfile": "mesh.msh",
            },
        },
        {
            "process": ModelProc,
            "required_paths": {
                "infile": "mesh.msh",
            },
            "output_paths": {
                "outfile": "model.vtk",
            },
        },
        {
            "process": SolverProc,
            "user_params": {
                "mass": "mass",
            },
            "hard_params": {
                "young": 1.2e6,
                "poisson": 0.0,
                "force": 4.0,
            },
            "user_paths": {
                "mesh_settings_file": "mesh_settings.json",
                "time_settings_file": "time_settings.json",
                "solver_settings_file": "solver_settings.json",
            },
            "required_paths": {
                "mesh_file": "mesh.msh",
                "model_file": "model.vtk",
            },
            "output_paths": {
                "outdir": "solution",
            },
        },
        {
            "process": PostProc,
            "required_paths": {
                "model_file": "model.vtk",
                "solution_dir": "solution",
            },
            "output_paths": {
                "data_file": "metrics.xlsx",
                "fig_file": "deflection.png",
            },
        },
        {
            "process": AnalysisProc,
            "overall_analysis": {
                "data_file": "metrics.xlsx",
            },
            "output_paths": {
                "fig_file": "overall_comparisons.png",
                "error_file": "overall_errors.csv",
            },
            "settings": {
                "add": True,
                "color": "red",
                "linestyle": "-",
                "linewidth": 1.5,
                "label": ""
            },
        },
    ]

    # ----------------------------------- #
    # Define default values of parameters #
    # ----------------------------------- #
    default_params = {
        "mass": 5.0,
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