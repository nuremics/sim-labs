# PostProc

<p align="left">
  <img src="https://img.shields.io/badge/NumPy-2.4.2+-4dabcf?style=flat&logo=numpy&logoColor=white" />

  <img src="https://img.shields.io/badge/PyVista-0.47.1+-00b25e" />
  <img src="https://img.shields.io/badge/Pandas-2.1.1+-0b0153?style=flat&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/openpyxl-3.1.5+-010043" />
</p>

## Process

Post-process simulation results to extract relevant metrics.<br>
A/ **`get_deflection`:** Extract the displacement at the extremity of the object from raw simulation results and save it to a metric data file.<br>
B/ **`plot_deflection`:** Plot the displacement metric over time.

```mermaid
erDiagram
  **Parameters** ||--|| **Inputs** : provides
  **Paths** ||--|| **Inputs** : provides
  **Inputs** ||--|| **PostProc** : feeds
  **PostProc** ||--|| **Outputs** : generates

  **Parameters** {
    _ _
  }
  **Paths** {
    file model_file "vtk"
    folder solution_dir "_"
  }
  **PostProc** {
    op get_deflection
    op plot_deflection
  }
  **Outputs** {
    file data_file "xlsx"
    file fig_file "png"
  }
```

## Input Parameter(s)

NA

## Input Path(s)

- **`model_file`:** File containing the model object.
- **`solution_dir`:** Directory containing the simulation results.

## Output Path(s)

- **`data_file`:** File containing the computed displacement metric.
- **`fig_file`:** File containing the visual representation of the displacement metric.