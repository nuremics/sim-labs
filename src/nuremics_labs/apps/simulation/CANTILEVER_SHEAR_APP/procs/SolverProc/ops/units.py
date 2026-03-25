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