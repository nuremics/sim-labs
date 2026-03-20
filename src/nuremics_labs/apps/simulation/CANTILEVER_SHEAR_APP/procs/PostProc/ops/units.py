import os
import re
import glob
import shutil
from pathlib import Path

import numpy as np
import pandas as pd
import pyvista as pv
import matplotlib.pyplot as plt


def get_deflection(
    model_file: str,
    solution_dir: Path,
    data_file: Path,
) -> None:
    """
    Build a VTK-based model object from a meshed geometry by creating
    data fields that map physical groups to their corresponding nodes 
    and elements.

    Parameters
    ----------
    infile : str
        Path to the mesh file (in Gmsh format) containing the meshed 
        geometry and physical group definitions.
    outfile : str
        Path to the model object (exported in VTK format).
    """

    mesh0: pv.UnstructuredGrid = pv.read(model_file)

    mask = mesh0.point_data["Load"] == 1
    ids_load = np.where(mask == True)[0].tolist()

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
            
            u_tip += np.abs(mesh.point_data["Displacement"][id, 0])/len(ids_load)
            w_tip += np.abs(mesh.point_data["Displacement"][id, 2])/len(ids_load)
        
        df.at[i, "Force"] /= 4.0
        df.at[i, "Utip"] = round(u_tip, 3)
        df.at[i, "Wtip"] = round(w_tip, 3)
        df.at[i, "Utip_ref"] = 3.286
        df.at[i, "Wtip_ref"] = 6.698
        df.at[i, "Error_Utip"] = 100.0*np.abs(df.at[i, "Utip"]-df.at[i, "Utip_ref"])/df.at[i, "Utip_ref"]
        df.at[i, "Error_Wtip"] = 100.0*np.abs(df.at[i, "Wtip"]-df.at[i, "Wtip_ref"])/df.at[i, "Wtip_ref"]
    
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
            "color": ["b", "b", "r", "r"],
            "zorder": None,
        },
    ]

    _plot_xy(
        list_plots=list_plots,
        config=(1, 1),
        size=(6, 4),
        save_png=fig_file,
    )


def _plot_xy(
    list_plots: list,
    config: tuple,
    size: tuple,
    save_pdf: str = None,
    save_png: str = None,
):
    """
    Plots two columns from a DataFrame as x and y axes.

    Parameters:
    df (pd.DataFrame): The pandas DataFrame containing the data.
    x_column (str): The name of the column to be used as the x-axis.
    y_column (str): The name of the column to be used as the y-axis.
    title (str): The title of the plot.
    x_label (str): The label for the x-axis.
    y_label (str): The label for the y-axis.
    legend_label (str, optional): The label for the legend. If None, no legend is displayed.
    save_pdf (str, optional): The file name for saving the plot as a PDF. If None, the plot is not saved as a PDF.
    save_png (str, optional): The file name for saving the plot as a PNG. If None, the plot is not saved as a PNG.

    Returns:
    None
    """
    fig, ax = plt.subplots(config[0], config[1])
    ax = np.atleast_1d(ax).ravel()
    fig.set_size_inches(size[0], size[1])

    for i, plot in enumerate(list_plots):
        
        x_column = plot["x_column"]
        y_column = plot["y_column"]
        title = plot["title"]
        x_label = plot["x_label"]
        y_label = plot["y_label"]
        marker = plot["marker"]
        linestyle = plot["linestyle"]
        color = plot["color"]
        label = plot["label"]
        zorder = plot["zorder"]

        for j, df in enumerate(plot["df"]):
        
            x_data = df[x_column[j]]
            y_data = df[y_column[j]]

            if label is not None:
                this_label = label[j]
            else:
                this_label = label

            if marker is not None:
                this_marker = marker[j]
            else:
                this_marker = marker

            if linestyle is not None:
                this_linestyle = linestyle[j]
            else:
                this_linestyle = linestyle
            
            if color is not None:
                this_color = color[j]
            else:
                this_color = color
            
            if zorder is not None:
                this_zorder = zorder[j]
            else:
                this_zorder = zorder
        
            ax[i].plot(x_data, y_data,
                marker=this_marker,
                linestyle=this_linestyle,
                color=this_color,
                label=this_label,
                zorder=this_zorder,
            )

        if title is not None:
            ax[i].set_title(title)
        if x_label is not None:
            ax[i].set_xlabel(x_label)
        if y_label is not None:
            ax[i].set_ylabel(y_label)
        ax[i].grid(True)

        # Check if a legend label is provided
        if label is not None:
            ax[i].legend()  # Display the legend if a label is given
            ax[i].legend(
                loc="center left",
                bbox_to_anchor=(1, 0.5)
            )

    # Save the plot as a PDF if save_pdf is specified
    if save_pdf is not None:
        plt.savefig(save_pdf, format="pdf")
    
    # Save the plot as a PNG if save_png is specified
    if save_png is not None:
        plt.savefig(save_png,
            format="png",
            dpi=300,
            bbox_inches="tight",
        )
    
    plt.close()