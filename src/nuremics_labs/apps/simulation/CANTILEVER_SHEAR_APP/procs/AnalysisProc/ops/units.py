from pathlib import Path

import pandas as pd
from nuremics import Process

from nuremics_labs.deps.plotting import (
    plot_xy,
)


@Process.analysis_function
def plot_overall(
    output: dict,
    settings: dict,
    filename: str,
) -> None:
    """
    Generate overall comparative plots of simulated (model) and theoritical trajectories.

    This function loads (x, y) trajectory data from a results file ("results.xlsx")
    and compares the model prediction to the theoretical reference for multiple 
    scenarios.

    Parameters
    ----------
    output : dict (containing output path to analyze for each case)
        Each path should contain a 'results.xlsx' file with the columns:
        - 'x_theory', 'y_theory': Theoretical trajectory coordinates.
        - 'x_model', 'y_model': Model/simulated trajectory coordinates.
    
    settings : dict (containing analysis settings for each case)
        Each entry must contain:
        - 'add'   (bool): Whether to include the case in the plot.
        - 'line'  (str) : Line style used for plotting the model trajectory.
        - 'label' (str) : Label for the legend; if set to "Model", the case name is used.
    
    filename : str
        Path to the file where the generated plot image will be saved (PNG format recommended).
    silent : bool (default is False)
        If False, displays the plot interactively using a window (e.g. for inspection).
    """

    list_plots = [
        {
            "df": [],
            "x_column": [],
            "y_column": [],
            "title": None,
            "x_label": "Time",
            "y_label": "$U_{tip}$",
            "label": None,
            "marker": None,
            "linewidth": [],
            "linestyle": [],
            "color": [],
            "zorder": [],
        },
        {
            "df": [],
            "x_column": [],
            "y_column": [],
            "title": None,
            "x_label": "Time",
            "y_label": "$W_{tip}$",
            "label": [],
            "marker": None,
            "linewidth": [],
            "linestyle": [],
            "color": [],
            "zorder": [],
        },
    ]

    # Browse output for each case
    for i in range(len(list_plots)):

        # Flag to plot "Reference" label only once
        first = True

        for case, out in output.items():
            if not settings[case]["add"]:
                continue

            # Load results from Excel file
            df = pd.read_excel(Path(out))

            # Plot reference, only label the first one
            if first:
                list_plots[i]["df"].append(df)
                list_plots[i]["x_column"].append("Time")
                if i == 0:
                    list_plots[i]["y_column"].append("Utip_ref")
                else:
                    list_plots[i]["y_column"].append("Wtip_ref")
                    list_plots[i]["label"].append("Reference")
                list_plots[i]["color"].append("k")
                list_plots[i]["linestyle"].append("--")
                list_plots[i]["linewidth"].append(settings[case]["linewidth"])
                list_plots[i]["zorder"].append(3)
            
            # Plot solution
            list_plots[i]["df"].append(df)
            list_plots[i]["x_column"].append("Time")
            if i == 0:
                list_plots[i]["y_column"].append("Utip")
            else:
                list_plots[i]["y_column"].append("Wtip")
                if settings[case]["label"] == "":
                    list_plots[i]["label"].append(case)
                else:
                    list_plots[i]["label"].append(settings[case]["label"])
            list_plots[i]["color"].append(settings[case]["color"])
            list_plots[i]["linestyle"].append("-")
            list_plots[i]["linewidth"].append(settings[case]["linewidth"])
            list_plots[i]["zorder"].append(4)

            first = False

    plot_xy(
        list_plots=list_plots,
        config=(1, 2),
        size=(10, 4),
        save_png=filename,
    )


@Process.analysis_function
def summarize_overall_errors(
    output: dict,
    settings: dict,
    filename: str,
) -> None:
    """
    Generate overall comparative plots of simulated (model) and theoritical trajectories.

    This function loads (x, y) trajectory data from a results file ("results.xlsx")
    and compares the model prediction to the theoretical reference for multiple 
    scenarios.

    Parameters
    ----------
    output : dict (containing output path to analyze for each case)
        Each path should contain a 'results.xlsx' file with the columns:
        - 'x_theory', 'y_theory': Theoretical trajectory coordinates.
        - 'x_model', 'y_model': Model/simulated trajectory coordinates.
    
    settings : dict (containing analysis settings for each case)
        Each entry must contain:
        - 'add'   (bool): Whether to include the case in the plot.
        - 'line'  (str) : Line style used for plotting the model trajectory.
        - 'label' (str) : Label for the legend; if set to "Model", the case name is used.
    
    filename : str
        Path to the file where the generated plot image will be saved (PNG format recommended).
    silent : bool (default is False)
        If False, displays the plot interactively using a window (e.g. for inspection).
    """

    rows = []
    
    # Browse output for each case
    for case, out in output.items():

        # Load results from Excel file
        df = pd.read_excel(Path(out))

        rows.append({
            "ID": case,
            "Error_Utip": df["Error_Utip"].iloc[-1],
            "Error_Wtip": df["Error_Wtip"].iloc[-1],
        })

    df_error = pd.DataFrame(rows)
    df_error = df_error.set_index("ID")
    df_error.to_csv(filename)