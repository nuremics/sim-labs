from importlib.resources import files
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from nuremics import Process


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
    
    # Flag to plot "Reference" label only once
    first = True

    # Define plot
    fig, ax = plt.subplots()
    
    # Browse output for each case
    for case, out in output.items():
        if not settings[case]["add"]:
            continue

        # Load results from Excel file
        df = pd.read_excel(Path(out))

        # Extract line style and label for the case
        color = settings[case]["color"]
        linestyle = settings[case]["linestyle"]
        linewidth = settings[case]["linewidth"]
        label = settings[case]["label"]
        if label == "":
            label = case
        
        # Plot reference, only label the first one
        if first:
            ax.plot(df["Time"], df["Utip_ref"], "k",
                zorder=3,
                linewidth=linewidth,
                label="Reference",
            )
        else:
            ax.plot(df["Time"], df["Utip_ref"], "k",
                zorder=3,
                linewidth=linewidth,
            )
        
        # Plot solution
        ax.plot(df["Time"], df["Utip"],
            color=color,
            linestyle=linestyle,
            linewidth=linewidth,
            label=label,
            zorder=4,
        )

        first = False
    
    # Set axis labels
    ax.set_xlabel("Time", fontsize=14)
    ax.set_ylabel("Deflection", fontsize=14)

    ax.grid(True)

    # Set equal aspect ratio, legend and grid
    ax.legend(
        fontsize=14,
        loc="center left",
        bbox_to_anchor=(1, 0.5),
    )

    # Save the plot to the specified file (with high resolution)
    fig.savefig(
        fname=filename,
        dpi=300,
        bbox_inches="tight",
    )
    
    # Close the figure to release memory
    plt.close(fig)