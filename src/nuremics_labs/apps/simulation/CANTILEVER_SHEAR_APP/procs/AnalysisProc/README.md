# AnalysisProc

<p align="left">
  <img src="https://img.shields.io/badge/Pandas-2.1.1+-0b0153?style=flat&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/openpyxl-3.1.5+-010043" />
  <img src="https://img.shields.io/badge/matplotlib-3.9.4+-11557c" />
</p>

## Process

Analyze the results of multiple simulation runs to identify trends, compare metrics, and draw conclusions.<br>
A/ **`plot_overall`:** Visualize and compare the metrics of the various simulation runs on a single plot.<br>
B/ **`summarize_overall_errors`:** Compile and summarize the deviations between computed simulation results and reference solutions for all performed tests.

```mermaid
erDiagram
  **Analysis** ||--|| **Inputs** : provides
  **Inputs** ||--|| **AnalysisProc** : feeds
  **AnalysisProc** ||--|| **Outputs** : generates

  **Analysis** {
    file data_file "xlsx"
  }
  **AnalysisProc** {
    op plot_overall
    op summarize_overall_errors
  }
  **Outputs** {
    file fig_file "png"
    file error_file "csv"
  }
```

## Input Analysis

- **`data_file`:** File containing the computed displacement metric.

## Output Path(s)

- **`fig_file`:** File containing the visual comparisons of the metrics for the various simulation runs.
- **`error_file`:** File summarizing the obtained errors across all simulation runs.