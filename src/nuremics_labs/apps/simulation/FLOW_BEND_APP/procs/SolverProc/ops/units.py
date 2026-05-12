import os
import subprocess
from pathlib import Path

import pyvista as pv
import numpy as np

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


def create_animation(
    solution_dir: Path,
):

    mesh0 = pv.read(solution_dir / "mesh.msh")

    reader = pv.get_reader(solution_dir / "dump" / "u.pvd")
    times = reader.time_values

    reader.set_active_time_point(len(times) - 1)
    mesh = reader.read()[0]
    u_max = np.max(
        np.linalg.norm(
            mesh.point_data["u"],
            axis=1,
        )
    )

    reader.set_active_time_point(0)
    mesh = reader.read()[0]

    slice_mesh = mesh.slice(
        normal=[0, 1, 0],
        origin=[0, 0, 0],
    )
    velocity_magnitude = np.linalg.norm(
        slice_mesh.point_data["u"],
        axis=1,
    )
    slice_mesh["velocity_magnitude"] = velocity_magnitude

    plotter = pv.Plotter(off_screen=True)
    plotter.add_mesh(
        mesh0,
        color="white",
        culling="front",
        specular=0.3,
    )
    plotter.add_mesh(
        slice_mesh,
        cmap="jet",
        lighting=False,
        clim=[0.0, u_max],
        scalars="velocity_magnitude",
        scalar_bar_args={
            "title": "u Magnitude",
        },
    )
    text_actor = plotter.add_text(
        "",
        position="upper_right",
        font_size=14,
        color="black",
    )
    plotter.view_xz()

    plotter.open_movie(
        filename=solution_dir / "animation.mp4",
        framerate=len(times) / 5,
    )
    for i, t in enumerate(times):

        reader.set_active_time_point(i)
        mesh = reader.read()[0]

        new_slice = mesh.slice(
            normal=[0, 1, 0],
            origin=[0, 0, 0],
        )
        velocity_magnitude = np.linalg.norm(
            new_slice.point_data["u"],
            axis=1,
        )
        slice_mesh.copy_from(new_slice)
        slice_mesh["velocity_magnitude"] = velocity_magnitude

        text_actor.set_text(
            position="upper_right",
            text=f"t = {t:.3f}",
        )

        plotter.write_frame()

    plotter.close()


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