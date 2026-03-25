from pathlib import Path

import numpy as np
import pandas as pd
import pyvista as pv

from nuremics_labs.deps.plotting import (
    plot_xy,
)


def get_deflection(
    model_file: str,
    solution_dir: Path,
    data_file: Path,
) -> None:

    mesh0: pv.UnstructuredGrid = pv.read(model_file)

    mask = mesh0.point_data["Load"] == 1
    ids_load = np.where(mask)[0].tolist()

    reader = pv.get_reader(str(solution_dir / "solution.pvd"))
    times = reader.time_values

    df = pd.read_excel(str(solution_dir / ".." / "force_record.xlsx"))
    df["Utip"] = None
    df["Wtip"] = None
    df["Utip_ref"] = None
    df["Wtip_ref"] = None
    df["Error_Utip"] = None
    df["Error_Wtip"] = None

    for i, _ in enumerate(times):

        reader.set_active_time_point(i)
        mesh: pv.UnstructuredGrid = reader.read()[0]
        u_tip = 0.0
        w_tip = 0.0
        
        for id in ids_load:
            
            u_tip += np.abs(mesh.point_data["Displacement"][id, 0]) / len(ids_load)
            w_tip += np.abs(mesh.point_data["Displacement"][id, 2]) / len(ids_load)
        
        df.at[i, "Force"] /= 4.0
        df.at[i, "Utip"] = round(u_tip, 3)
        df.at[i, "Wtip"] = round(w_tip, 3)
        df.at[i, "Utip_ref"] = 3.286
        df.at[i, "Wtip_ref"] = 6.698
        df.at[i, "Error_Utip"] = 100.0 * np.abs(df.at[i, "Utip"] - df.at[i, "Utip_ref"]) / df.at[i, "Utip_ref"]
        df.at[i, "Error_Wtip"] = 100.0 * np.abs(df.at[i, "Wtip"] - df.at[i, "Wtip_ref"]) / df.at[i, "Wtip_ref"]
    
    df.to_excel(
        excel_writer=data_file,
        index=False
    )

    return df


def plot_deflection(
    df: pd.DataFrame,
    fig_file: str,
) -> None:

    list_plots = [
        {
            "df": [df, df, df, df],
            "x_column": ["Time", "Time", "Time", "Time"],
            "y_column": ["Utip", "Utip_ref", "Wtip", "Wtip_ref"],
            "title": None,
            "x_label": "Time",
            "y_label": "Deflection",
            "label": ["$U_{tip}$ (solution)", "$U_{tip}$ (reference)", "$W_{tip}$ (solution)", "$W_{tip}$ (reference)"],
            "marker": None,
            "linestyle": ["-", "--", "-", "--"],
            "linewidth": [1.5, 1.5, 1.5, 1.5],
            "color": ["b", "b", "r", "r"],
            "zorder": None,
        },
    ]

    plot_xy(
        list_plots=list_plots,
        config=(1, 1),
        size=(6, 4),
        save_png=fig_file,
    )