import os
import attrs
import json
from pathlib import Path

from nuremics import Process
from nuremics_labs.apps.simulation.CANTILEVER_SHEAR_APP.procs.SolverProc.ops import (
   run_solver,
   compile_solution,
)


@attrs.define
class SolverProc(Process):
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

    # Parameters
    mass: float = attrs.field(init=False, metadata={"input": True})
    young: float = attrs.field(init=False, metadata={"input": True})
    poisson: float = attrs.field(init=False, metadata={"input": True})
    force: float = attrs.field(init=False, metadata={"input": True})

    # Paths
    mesh_settings_file: Path = attrs.field(init=False, metadata={"input": True}, converter=Path)
    solver_settings_file: Path = attrs.field(init=False, metadata={"input": True}, converter=Path)
    mesh_file: Path = attrs.field(init=False, metadata={"input": True}, converter=Path)
    model_file: Path = attrs.field(init=False, metadata={"input": True}, converter=Path)

    # Outputs
    outdir: Path = attrs.field(init=False, metadata={"output": True}, converter=Path)

    # Internal
    dict_solver_settings: dict = attrs.field(init=False)

    def __call__(self):
        super().__call__()

        self.run_solver()
        self.compile_solution()

    def run_solver(self):
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

        with open(self.mesh_settings_file) as f:
            dict_mesh_settings = json.load(f)
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
            dt=self.dict_solver_settings["dt"],
            ramp=self.dict_solver_settings["ramp"],
            scheme=self.dict_solver_settings["scheme"],
            solver=self.dict_solver_settings["solver"],
            results_path=self.outdir,
            silent=True,
        )

    def compile_solution(self):
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