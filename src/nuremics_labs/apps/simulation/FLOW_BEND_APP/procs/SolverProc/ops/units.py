import os
import subprocess
from pathlib import Path

DOCKER_IMAGE = "dolfinx/dolfinx:stable"


def run_solver(
    mesh_file: str,
    r: float,
    R: float,
    u_mean: float,
    rho: float,
    mu: float,
    t_final: float,
    dt: float,
    ramp: float,
    solution_dir: str,
):
    
    fenicsx_script_path = Path(__file__).parent / "fenicsx.py"

    _run_fenicsx(
        script_path=fenicsx_script_path,
        mesh_file=mesh_file,
        r=r,
        R=R,
        u_mean=u_mean,
        rho=rho,
        mu=mu,
        t_final=t_final,
        dt=dt,
        ramp=ramp,
        solution_dir=solution_dir,
    )

def _run_fenicsx(
    script_path: str,
    mesh_file: str,
    r: float,
    R: float,
    u_mean: float,
    rho: float,
    mu: float,
    t_final: float,
    dt: float,
    ramp: float,
    solution_dir: str,
):

    cwd = Path.cwd().resolve()
    script_path = Path(script_path).resolve()

    input_path = Path(os.path.split(mesh_file)[0]).resolve()
    input_file = os.path.split(mesh_file)[1]

    cmd = [
        "docker", "run", "--rm",
        "-v", f"{script_path.parent}:/work",
        "-v", f"{cwd}/{solution_dir}:/output",
        "-v", f"{input_path}:/input",
        "-w", "/work",
        DOCKER_IMAGE,
        "mpirun", "-n", "10",
        "python3", script_path.name,
        input_file, str(r), str(R), str(u_mean), str(rho), str(mu), str(t_final), str(dt), str(ramp),
    ]
    subprocess.run(cmd, check=True)