import glob
import os
import re
import shutil
from pathlib import Path

import numpy as np
import pyvista as pv

from nuremics_labs.apps.simulation.CANTILEVER_SHEAR_APP.procs.SolverProc.ops.sofa import main as sofa


def run_solver(
    mesh_file: str,
    model_file: str,
    mass: float,
    young: float,
    poisson: float,
    force: float,
    elem: str,
    ramp: float,
    final_time: float,
    dt: float,
    scheme: str,
    solver: str,
    results_path: Path,
    silent: bool,
) -> None:

    dump_path = results_path / "dump"
    if dump_path.exists():
        shutil.rmtree(dump_path) 
    
    dump_path.mkdir(
        exist_ok=True,
        parents=True,
    )

    sofa(
        mesh_file=mesh_file,
        model_file=model_file,
        mass=mass,
        young=young,
        poisson=poisson,
        force=force,
        elem=elem,
        ramp=ramp,
        final_time=final_time,
        dt=dt,
        scheme=scheme,
        solver=solver,
        dump_path=dump_path,
        silent=silent,
    )


def compile_solution(
    dt: float,
    results_path: Path,
    output_path: Path,
) -> None:

    def _extract_number(filename: str) -> int:
        match = re.search(r'solution(\d+)\.vtu$', filename)
        return int(match.group(1)) if match else -1

    results = glob.glob(str(results_path / "dump" / "solution*.vtu"))
    results = sorted(results, key=_extract_number)

    _compute_displacement_field(
        results=results,
    )

    # Create content of the .pvd file
    pvd_content = '<?xml version="1.0"?>\n'
    pvd_content += '<VTKFile type="Collection" version="0.1" byte_order="LittleEndian">\n'
    pvd_content += '  <Collection>\n'

    for timestep, vtu_file in enumerate(results):
        # Add .vtu file with a time step
        t = timestep * dt
        pvd_content += f'    <DataSet timestep="{t}" group="" part="0" file="dump/{os.path.basename(vtu_file)}"/>\n'

    pvd_content += '  </Collection>\n'
    pvd_content += '</VTKFile>\n'

    # Write content within the .pvd file
    with open(output_path, "w") as pvd_file:
        pvd_file.write(pvd_content)


def create_animation(
    solution_dir: Path,
) -> None:

    reader = pv.get_reader(solution_dir / "solution.pvd")
    times = reader.time_values

    reader.set_active_time_point(0)
    mesh = reader.read()[0]

    mesh0 = pv.read(solution_dir / "dump" / "solution0.vtu")
    mesh1 = pv.read(solution_dir / "dump" / f"solution{len(times) - 1}.vtu")

    mesh["Z Displacement"] = mesh.point_data["Displacement"][:, 2]

    plotter = pv.Plotter(off_screen=True)
    plotter.add_mesh(
        mesh=mesh0,
        color="white",
        opacity=0.2,
    )
    plotter.add_mesh(
        mesh=mesh1,
        color="white",
        opacity=0.0,
    )
    plotter.add_mesh(
        mesh=mesh,
        lighting=False,
        cmap="viridis",
        clim=[0.0, 6.698],
        scalars="Z Displacement",
        scalar_bar_args={
            "title": "Z Displacement",
        },
    )
    text_actor = plotter.add_text(
        "",
        position="upper_right",
        font_size=14,
        color="black",
    )
    plotter.view_xz()
    plotter.camera.azimuth = 30
    plotter.camera.elevation = 10
    plotter.reset_camera_clipping_range()

    plotter.open_movie(
        filename=solution_dir / "animation.mp4",
        framerate=len(times) / 5,
    )
    for i, t in enumerate(times):

        reader.set_active_time_point(i)
        new_mesh = reader.read()[0]

        mesh.copy_from(new_mesh)
        mesh["Z Displacement"] = new_mesh.point_data["Displacement"][:, 2]
        mesh.set_active_scalars("Z Displacement")
        
        text_actor.set_text(
            position="upper_right",
            text=f"t = {t:.3f}",
        )

        plotter.write_frame()

    plotter.close()


def _compute_displacement_field(
    results: list,
) -> None:
    
    mesh0: pv.UnstructuredGrid = pv.read(results[0])

    for vtu_file in results:

        mesh: pv.UnstructuredGrid = pv.read(vtu_file)
        mesh.point_data["Displacement"] = np.zeros((mesh.n_points, 3), dtype=float)

        for i in range(mesh.n_points):
            mesh.point_data["Displacement"][i, :] = mesh.points[i, :] - mesh0.points[i, :]
        
        mesh.save(
            filename=vtu_file,
            binary=False,
        )