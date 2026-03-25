import json
import os
from pathlib import Path

import attrs
from nuremics import Process

from nuremics_labs.apps.simulation.CANTILEVER_SHEAR_APP.procs.SolverProc.ops import (
    compile_solution,
    run_solver,
)


@attrs.define
class SolverProc(Process):
    """
    Compute the mechanical deformation of a physical system under prescribed 
    boundary conditions.

    Process
    -------
        A/ run_solver: 
            Define the simulation setup, apply boundary conditions, and execute 
            the solver to compute the raw simulation results.
        B/ compile_solution:
            Compile the raw simulation results into a PVD format and compute 
            the displacement field over the model.

    Input parameters
    ----------------
        mass: float
            Mass of the material.
        young: float
            Young's modulus of the material. 
        poisson: float
            Poisson's ratio of the material.
        force: float
            Magnitude of the external force applied to the system as a
            boundary condition.

    Input paths
    -----------
        mesh_settings_file: json
            File containing the mesh discretization settings.
        time_settings_file: json
            File containing the time settings.
        solver_settings_file: json
            File containing the solver settings.
        mesh_file: msh
            File containing the meshed geometry and physical group definitions (in Gmsh format).
        model_file: vtk
            File containing the model object.

    Outputs
    -------
        outdir: folder
            Directory containing the simulation results.
    """

    # Parameters
    mass: float = attrs.field(init=False, metadata={"input": True})
    young: float = attrs.field(init=False, metadata={"input": True})
    poisson: float = attrs.field(init=False, metadata={"input": True})
    force: float = attrs.field(init=False, metadata={"input": True})

    # Paths
    mesh_settings_file: Path = attrs.field(init=False, metadata={"input": True}, converter=Path)
    time_settings_file: Path = attrs.field(init=False, metadata={"input": True}, converter=Path)
    solver_settings_file: Path = attrs.field(init=False, metadata={"input": True}, converter=Path)
    mesh_file: Path = attrs.field(init=False, metadata={"input": True}, converter=Path)
    model_file: Path = attrs.field(init=False, metadata={"input": True}, converter=Path)

    # Outputs
    outdir: Path = attrs.field(init=False, metadata={"output": True}, converter=Path)

    # Internal
    dict_solver_settings: dict = attrs.field(init=False)

    def __call__(self) -> None:
        super().__call__()

        self.run_solver()
        self.compile_solution()

    def run_solver(self) -> None:
        """
        Compute the mechanical deformation of a physical system under prescribed 
        boundary conditions.

        Uses
        ----
            mesh_settings_file
            time_settings_file
            solver_settings_file
        
        Generates
        ---------
            outdir
            dict_solver_settings
        """

        with open(self.mesh_settings_file) as f:
            dict_mesh_settings = json.load(f)
        with open(self.time_settings_file) as f:
            dict_time_settings = json.load(f)
        with open(self.solver_settings_file) as f:
            self.dict_solver_settings = json.load(f)

        self.outdir.mkdir(
            exist_ok=True,
            parents=True,
        )

        run_solver(
            mesh_file=str(self.mesh_file),
            model_file=str(self.model_file),
            mass=self.mass,
            young=self.young,
            poisson=self.poisson,
            force=self.force,
            elem=dict_mesh_settings["elem"],
            ramp=dict_time_settings["ramp"],
            final_time=dict_time_settings["final_time"],
            dt=self.dict_solver_settings["dt"],
            scheme=self.dict_solver_settings["scheme"],
            solver=self.dict_solver_settings["solver"],
            results_path=self.outdir,
            silent=True,
        )

    def compile_solution(self) -> None:
        """
        Compile the raw simulation results into a PVD format and compute 
        the displacement field over the model.

        Uses
        ----
            dict_solver_settings
        
        Generates
        ---------
            outdir
        """

        compile_solution(
            dt=self.dict_solver_settings["dt"],
            results_path=self.outdir,
            output_path=self.outdir / "solution.pvd",
        )


if __name__ == "__main__":

    # ================================================================== #
    #                      USER-DEFINED PARAMETERS                       #
    #              >>>>> TO BE EDITED BY THE OPERATOR <<<<<              #
    # ================================================================== #

    # Working directory
    working_dir = Path(r"...")

    # Input parameters
    mass = 5.0
    young = 1.2e6
    poisson = 0.0
    force = 4.0

    # Input paths
    mesh_settings_file = Path(r"...")
    time_settings_file = Path(r"...")
    solver_settings_file = Path(r"...")
    mesh_file = Path(r"...")
    model_file = Path(r"...")

    # Output paths
    outdir = "solution"

    # ================================================================== #

    # Go to working directory
    os.chdir(working_dir)

    # Create dictionary containing input data
    dict_inputs = {
        "mass": mass,
        "young": young,
        "poisson": poisson,
        "force": force,
        "mesh_settings_file": mesh_settings_file,
        "time_settings_file": time_settings_file,
        "solver_settings_file": solver_settings_file,
        "mesh_file": mesh_file,
        "model_file": model_file,
        "outdir": outdir,
    }

    # Create process
    process = SolverProc(
        dict_inputs=dict_inputs,
        set_inputs=True,
    )

    # Run process
    process()
    process.finalize()