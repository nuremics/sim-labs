import os
import shutil
from pathlib import Path

import attrs
from nuremics import Process

from nuremics_labs.apps.simulation.FLOW_BEND_APP.procs.SolverProc.ops import (
    run_solver,
)


@attrs.define
class SolverProc(Process):

    # Parameters
    r: float = attrs.field(init=False, metadata={"input": True})
    R: float = attrs.field(init=False, metadata={"input": True})
    u_mean: float = attrs.field(init=False, metadata={"input": True})
    rho: float = attrs.field(init=False, metadata={"input": True})
    mu: float = attrs.field(init=False, metadata={"input": True})
    t_final: float = attrs.field(init=False, metadata={"input": True})
    dt: float = attrs.field(init=False, metadata={"input": True})
    ramp: float = attrs.field(init=False, metadata={"input": True})

    # Paths
    mesh_file: Path = attrs.field(init=False, metadata={"input": True}, converter=Path)
    
    # Outputs
    outdir: Path = attrs.field(init=False, metadata={"output": True}, converter=Path)

    def __call__(self) -> None:
        super().__call__()

        self.run_solver()

    def run_solver(self) -> None:

        if self.outdir.exists():
            shutil.rmtree(self.outdir)

        self.outdir.mkdir(
            exist_ok=True,
            parents=True,
        )

        shutil.copy(
            src=self.mesh_file,
            dst=self.outdir / os.path.split(self.mesh_file)[1],
        )

        run_solver(
            mesh_file=str(self.mesh_file),
            r=self.r,
            R=self.R,
            u_mean=self.u_mean,
            rho=self.rho,
            mu=self.mu,
            t_final=self.t_final,
            dt=self.dt,
            ramp=self.ramp,
            solution_dir=str(self.outdir),
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
    R = 5.0
    u_mean = 1.0
    rho = 1.0e-3 * 1.1e3
    mu = 10.0 * 3.6e-3
    t_final = 50.0
    dt = t_final / 100.0
    ramp = 5.0

    # Input paths
    mesh_file = Path(r"C:\Users\julie\Documents\nuRemics\test") / "mesh.msh"

    # Output paths
    outdir = "solution"

    # ================================================================== #

    # Go to working directory
    os.chdir(working_dir)

    # Create dictionary containing input data
    dict_inputs = {
        "r": r,
        "R": R,
        "u_mean": u_mean,
        "rho": rho,
        "mu": mu,
        "t_final": t_final,
        "dt": dt,
        "ramp": ramp,
        "mesh_file": mesh_file,
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