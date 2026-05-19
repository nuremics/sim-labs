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

    list_plots = [
        {
            "df": [],
            "x_column": [],
            "y_column": [],
            "title": "Upstream",
            "x_label": "Inner to ➝ Outer wall",
            "y_label": "u Magnitude",
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
            "title": "Downstream",
            "x_label": "Inner to ➝ Outer wall",
            "y_label": None,
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

        for case, out in output.items():
            if not settings[case]["add"]:
                continue

            # Load results
            df = pd.read_csv(Path(out))
            
            # Plot solution
            list_plots[i]["df"].append(df)
            list_plots[i]["x_column"].append("s")
            if i == 0:
                list_plots[i]["y_column"].append("upstream")
            else:
                list_plots[i]["y_column"].append("downstream")
                if settings[case]["label"] == "":
                    list_plots[i]["label"].append(case)
                else:
                    list_plots[i]["label"].append(settings[case]["label"])
            list_plots[i]["color"].append(settings[case]["color"])
            list_plots[i]["linestyle"].append("-")
            list_plots[i]["linewidth"].append(settings[case]["linewidth"])
            list_plots[i]["zorder"].append(4)

    plot_xy(
        list_plots=list_plots,
        config=(1, 2),
        size=(10, 4),
        logo=True,
        save_png=filename,
    )