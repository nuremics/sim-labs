from pathlib import Path

import numpy as np
import pandas as pd
import pyvista as pv

from nuremics_labs.deps.plotting import (
    plot_xy,
)


def get_probes_velocity(
    r: float,
    solution_dir: Path,
    data_file: Path,
) -> None:

    probe_points = np.array([
        [ 0.5 * r, 0.0, 0.0],
        [     0.0, 0.0, 0.0],
        [-0.5 * r, 0.0, 0.0],
    ])
    probes = pv.PolyData(probe_points)

    reader = pv.get_reader(solution_dir / "dump" / "u.pvd")
    times = reader.time_values

    rows = []
    for i, t in enumerate(times):

        reader.set_active_time_point(i)
        mesh = reader.read()[0]

        velocity_magnitude = np.linalg.norm(
            mesh.point_data["u"],
            axis=1,
        )
        mesh["velocity_magnitude"] = velocity_magnitude

        sampled = probes.sample(mesh)

        rows.append({
            "Time": t,
            "Probe 1": sampled.point_data["velocity_magnitude"][0],
            "Probe 2": sampled.point_data["velocity_magnitude"][1],
            "Probe 3": sampled.point_data["velocity_magnitude"][2],
        })
    
    df = pd.DataFrame(rows)

    df.to_csv(
        path_or_buf=data_file,
        index=False,
    )

    return df


def plot_probes_velocity(
    df: pd.DataFrame,
    fig_file: str,
) -> None:

    list_plots = [
        {
            "df": [df, df, df],
            "x_column": ["Time", "Time", "Time"],
            "y_column": ["Probe 1", "Probe 2", "Probe 3"],
            "title": None,
            "x_label": "Time",
            "y_label": "u Magnitude",
            "label": ["Probe 1", "Probe 2", "Probe 3"],
            "marker": None,
            "linestyle": ["-", "-", "-"],
            "linewidth": [1.5, 1.5, 1.5],
            "color": ["dodgerblue", "red", "limegreen"],
            "zorder": None,
        },
    ]

    plot_xy(
        list_plots=list_plots,
        config=(1, 1),
        size=(6, 4),
        logo=True,
        save_png=fig_file,
    )


def get_velocity_profiles(
    r: float,
    R: float,
    solution_dir: Path,
    data_file: Path,
) -> None:

    reader = pv.get_reader(solution_dir / "dump" / "u.pvd")
    times = reader.time_values

    reader.set_active_time_point(len(times) - 1)
    mesh = reader.read()[0]

    velocity_magnitude = np.linalg.norm(
        mesh.point_data["u"],
        axis=1,
    )
    mesh["velocity_magnitude"] = velocity_magnitude

    resolution = 200
    profile_upstream = mesh.sample_over_line(
        pointa=(R, 0.0, R - r),
        pointb=(R, 0.0, r + R),
        resolution=resolution,
    )
    profile_downstream = mesh.sample_over_line(
        pointa=(r, 0.0, 0.0),
        pointb=(-r, 0.0, 0.0),
        resolution=resolution,
    )

    s = profile_upstream["Distance"]
    s_normalized = s / s[-1]

    df = pd.DataFrame({
        "s": s_normalized,
        "upstream": profile_upstream["velocity_magnitude"],
        "downstream": profile_downstream["velocity_magnitude"],
    })
    df.to_csv(
        path_or_buf=data_file,
        index=False,
    )

    return df


def plot_velocity_profiles(
    df: pd.DataFrame,
    fig_file: str,
) -> None:

    list_plots = [
        {
            "df": [df, df],
            "x_column": ["s", "s"],
            "y_column": ["upstream", "downstream"],
            "title": None,
            "x_label": "Inner to ➝ Outer wall",
            "y_label": "u Magnitude",
            "label": ["Upstream", "Downstream"],
            "marker": None,
            "linestyle": ["-", "-"],
            "linewidth": [1.5, 1.5],
            "color": ["dodgerblue", "red"],
            "zorder": None,
        },
    ]

    plot_xy(
        list_plots=list_plots,
        config=(1, 1),
        size=(6, 4),
        logo=True,
        save_png=fig_file,
    )