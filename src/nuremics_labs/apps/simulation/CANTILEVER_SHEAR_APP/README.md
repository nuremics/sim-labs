# CANTILEVER_SHEAR_APP

<p align="left">
  <img src="https://img.shields.io/badge/pythonocc--core-7.4.0+-f7941e" />
  <img src="https://img.shields.io/badge/Gmsh-4.15.0+-ffffff" />
  <img src="https://img.shields.io/badge/meshio-5.3.5+-81ecec" />
  <img src="https://img.shields.io/badge/NumPy-2.4.2+-4dabcf?style=flat&logo=numpy&logoColor=white" />
  <img src="https://img.shields.io/badge/PyVista-0.47.1+-00b25e" />
  <img src="https://img.shields.io/badge/SOFA Framework-25.6.0-e84e1c" />
  <img src="https://img.shields.io/badge/Pandas-2.1.1+-0b0153?style=flat&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/openpyxl-3.1.5+-010043" />
  <img src="https://img.shields.io/badge/matplotlib-3.9.4+-11557c" />
</p>

## Workflow

1. **[`GeometryProc`](https://github.com/nuremics/sim-labs/tree/cantilever-shear/src/nuremics_labs/apps/simulation/CANTILEVER_SHEAR_APP/procs/GeometryProc):** Create a geometric representation of a physical system.<br>
  A/ **`create_geometry`:** Create and export a simple geometric entity (1D line, 2D rectangle or 3D box) in BREP format.
2. **[`LabelingProc`](https://github.com/nuremics/sim-labs/tree/cantilever-shear/src/nuremics_labs/apps/simulation/CANTILEVER_SHEAR_APP/procs/LabelingProc):** Define and label the entities of a physical system from its geometric representation.<br>
  A/ **`label_entities`:** Assign labels to the entities of a geometric model.
3. **[`MeshProc`](https://github.com/nuremics/sim-labs/tree/cantilever-shear/src/nuremics_labs/apps/simulation/CANTILEVER_SHEAR_APP/procs/MeshProc):** Discretize the geometric representation of a physical system into a computational mesh.<br>
  A/ **`generate_mesh`:** Generate and export a computational mesh from a geometric model by discretizing the domain into mesh entities (nodes, elements) and assigning labeled physical groups.
4. **[`ModelProc`](https://github.com/nuremics/sim-labs/tree/cantilever-shear/src/nuremics_labs/apps/simulation/CANTILEVER_SHEAR_APP/procs/ModelProc):** Convert a meshed geometry into a model object mapping geometric labels to mesh entities.<br>
  A/ **`build_model`:** Build a VTK-based model object from a meshed geometry by creating data fields that map physical groups to their corresponding nodes and elements.
5. **[`SolverProc`](https://github.com/nuremics/sim-labs/tree/cantilever-shear/src/nuremics_labs/apps/simulation/CANTILEVER_SHEAR_APP/procs/SolverProc):** Compute the mechanical deformation of a physical system under prescribed boundary conditions.<br>
  A/ **`run_solver`:** Define the simulation setup, apply boundary conditions, and execute the solver to compute the raw simulation results.<br>
  B/ **`compile_solution`:** Compile the raw simulation results into a PVD format and compute the displacement field over the model.
6. **[`PostProc`](https://github.com/nuremics/sim-labs/tree/cantilever-shear/src/nuremics_labs/apps/simulation/CANTILEVER_SHEAR_APP/procs/PostProc):** Post-process simulation results to extract relevant metrics.<br>
  A/ **`get_deflection`:** Extract the displacement at the extremity of the object from raw simulation results and save it to a metric data file.<br>
  B/ **`plot_deflection`:** Plot the displacement metric over time.
7. **[`AnalysisProc`](https://github.com/nuremics/sim-labs/tree/cantilever-shear/src/nuremics_labs/apps/simulation/CANTILEVER_SHEAR_APP/procs/AnalysisProc):** Analyze the results of multiple simulation runs to identify trends, compare metrics, and draw conclusions.<br>
  A/ **`plot_overall`:** Visualize and compare the metrics of the various simulation runs on a single plot.<br>
  B/ **`summarize_overall_errors`:** Compile and summarize the deviations between computed simulation results and reference solutions for all performed tests.

```mermaid
flowchart RL
  Proc1[<b>GeometryProc<b>] e1@--1--o App[<b>CANTILEVER_SHEAR_APP<b>]
  Proc2[<b>LabelingProc<b>] e2@--2--o App
  Proc3[<b>MeshingProc<b>] e3@--3--o App
  Proc4[<b>ModelProc<b>] e4@--4--o App
  Proc5[<b>SolverProc<b>] e5@--5--o App
  Proc6[<b>PostProc<b>] e6@--6--o App
  Proc7[<b>AnalysisProc<b>] e7@--7--o App
  Op11[<b>create_geometry<b>] e8@--A--o Proc1
  Op21[<b>label_entities<b>] e9@--A--o Proc2
  Op31[<b>generate_mesh<b>] e10@--A--o Proc3
  Op41[<b>build_model<b>] e11@--A--o Proc4
  Op51[<b>run_solver<b>] e12@--A--o Proc5
  Op52[<b>compile_solution<b>] e13@--B--o Proc5
  Op61[<b>get_deflection<b>] e14@--A--o Proc6
  Op62[<b>plot_deflection<b>] e15@--B--o Proc6
  Op71[<b>plot_overall<b>] e16@--A--o Proc7
  Op72[<b>summarize_overall_errors<b>] e17@--B--o Proc7
  e1@{ animate: true }
  e2@{ animate: true }
  e3@{ animate: true }
  e4@{ animate: true }
  e5@{ animate: true }
  e6@{ animate: true }
  e7@{ animate: true }
  e8@{ animate: true }
  e9@{ animate: true }
  e10@{ animate: true }
  e11@{ animate: true }
  e12@{ animate: true }
  e13@{ animate: true }
  e14@{ animate: true }
  e15@{ animate: true }
  e16@{ animate: true }
  e17@{ animate: true }
```

## Mapping

```mermaid
erDiagram
  **CANTILEVER_SHEAR_APP** ||--|| **hard_params** : mapping
  **CANTILEVER_SHEAR_APP** ||--|| **output_paths** : mapping
  **hard_params** ||--|| **GeometryProc** : mapping
  **output_paths** ||--|| **GeometryProc** : mapping

  **hard_params** {
    int dim "3"
    float length "10.0"
    float width "1.0"
    float height "0.1"
  }
  **output_paths** {
    file outfile "geometry.brep"
  }
```

```mermaid
erDiagram
  **CANTILEVER_SHEAR_APP** ||--|| **hard_params** : mapping
  **CANTILEVER_SHEAR_APP** ||--|| **required_paths** : mapping
  **CANTILEVER_SHEAR_APP** ||--|| **output_paths** : mapping
  **hard_params** ||--|| **LabelingProc** : mapping
  **required_paths** ||--|| **LabelingProc** : mapping
  **output_paths** ||--|| **LabelingProc** : mapping

  **hard_params** {
    int dim "3"
  }
  **required_paths** {
    file infile "geometry.brep"
  }
  **output_paths** {
    file outfile "labels.json"
  }
```

```mermaid
erDiagram
  **CANTILEVER_SHEAR_APP** ||--|| **hard_params** : mapping
  **CANTILEVER_SHEAR_APP** ||--|| **user_paths** : mapping
  **CANTILEVER_SHEAR_APP** ||--|| **required_paths** : mapping
  **CANTILEVER_SHEAR_APP** ||--|| **output_paths** : mapping
  **hard_params** ||--|| **MeshProc** : mapping
  **user_paths** ||--|| **MeshProc** : mapping
  **required_paths** ||--|| **MeshProc** : mapping
  **output_paths** ||--|| **MeshProc** : mapping

  **hard_params** {
    int dim "3"
  }
  **user_paths** {
    file mesh_settings_file "mesh_settings.json"
  }
  **required_paths** {
    file infile "labels.json"
  }
  **output_paths** {
    file outfile "mesh.msh"
  }
```

```mermaid
erDiagram
  **CANTILEVER_SHEAR_APP** ||--|| **required_paths** : mapping
  **CANTILEVER_SHEAR_APP** ||--|| **output_paths** : mapping
  **required_paths** ||--|| **ModelProc** : mapping
  **output_paths** ||--|| **ModelProc** : mapping

  **required_paths** {
    file infile "mesh.msh"
  }
  **output_paths** {
    file outfile "model.vtk"
  }
```

```mermaid
erDiagram
  **CANTILEVER_SHEAR_APP** ||--|| **user_params** : mapping
  **CANTILEVER_SHEAR_APP** ||--|| **hard_params** : mapping
  **CANTILEVER_SHEAR_APP** ||--|| **user_paths** : mapping
  **CANTILEVER_SHEAR_APP** ||--|| **required_paths** : mapping
  **CANTILEVER_SHEAR_APP** ||--|| **output_paths** : mapping
  **user_params** ||--|| **SolverProc** : mapping
  **hard_params** ||--|| **SolverProc** : mapping
  **user_paths** ||--|| **SolverProc** : mapping
  **required_paths** ||--|| **SolverProc** : mapping
  **output_paths** ||--|| **SolverProc** : mapping

  **user_params** {
    float mass "mass"
  }
  **hard_params** {
    int dim "3"
    float young "1.2e6"
    float poisson "0.0"
    float force "4.0"
  }
  **user_paths** {
    file mesh_settings_file "mesh_settings.json"
    file time_settings_file "time_settings.json"
    file solver_settings_file "solver_settings.json"
  }
  **required_paths** {
    file mesh_file "mesh.msh"
    file model_file "model.vtk"
  }
  **output_paths** {
    folder outdir "solution"
  }
```

```mermaid
erDiagram
  **CANTILEVER_SHEAR_APP** ||--|| **required_paths** : mapping
  **CANTILEVER_SHEAR_APP** ||--|| **output_paths** : mapping
  **required_paths** ||--|| **PostProc** : mapping
  **output_paths** ||--|| **PostProc** : mapping

  **required_paths** {
    file model_file "model.vtk"
    folder solution_dir "solution"
  }
  **output_paths** {
    file data_file "metrics.xlsx"
    file fig_file "deflection.png"
  }
```

```mermaid
erDiagram
  **CANTILEVER_SHEAR_APP** ||--|| **overall_analysis** : mapping
  **CANTILEVER_SHEAR_APP** ||--|| **output_paths** : mapping
  **overall_analysis** ||--|| **AnalysisProc** : mapping
  **output_paths** ||--|| **AnalysisProc** : mapping

  **overall_analysis** {
    file data_file "metrics.xlsx"
  }
  **output_paths** {
    file fig_file "overall_comparisons.png"
    file error_file "overall_errors.csv"
  }
```

## I/O Interface

```mermaid
flowchart LR
  subgraph Inputs[<b>INPUTS<b>]
    direction TB

    subgraph Paths[<b>Paths<b>]
      direction LR
      path1["mesh_settings.json <i>(file)<i>"]
      path2["time_settings.json <i>(file)<i>"]
      path3["solver_settings.json <i>(file)<i>"]
    end

    subgraph Parameters[<b>Parameters<b>]
      direction LR
      param1["mass"]
    end
  end

  subgraph App[<b>CANTILEVER_SHEAR_APP<b>]
    direction RL
    proc1["GeometryProc"]
    proc2["LabelingProc"]
    proc3["MeshProc"]
    proc4["ModelProc"]
    proc5["SolverProc"]
    proc6["PostProc"]
    proc7["AnalysisProc"]
  end

  subgraph Outputs[<b>OUTPUTS<b>]
    direction RL
    out1["geometry.brep <i>(file)<i>"]
    out2["labels.json <i>(file)<i>"]
    out3["mesh.msh <i>(file)<i>"]
    out4["model.vtk <i>(file)<i>"]
    out5["solution <i>(folder)<i>"]
    out6["metrics.xlsx <i>(file)<i>"]
    out7["overall_comparisons.png <i>(file)<i>"]
    out8["overall_errors.csv <i>(file)<i>"]
  end

  Inputs --> App
  App --> Outputs
```

```mermaid
flowchart LR
  subgraph Inputs[<b>INPUTS<b>]
    direction TB

    subgraph Paths[<b>Paths<b>]
      direction LR
      path["_"]
    end

    subgraph Parameters[<b>Parameters<b>]
      direction LR
      param1["_"]
    end
  end

  subgraph App[<b>CANTILEVER_SHEAR_APP<b>]
    direction RL
    proc["GeometryProc"]
  end

  subgraph Outputs[<b>OUTPUTS<b>]
    direction RL
    out1["geometry.brep <i>(file)<i>"]
  end

  Inputs --> proc
  proc --> Outputs
```

```mermaid
flowchart LR
  subgraph Inputs[<b>INPUTS<b>]
    direction TB

    subgraph Paths[<b>Paths<b>]
      direction LR
    path1["geometry.brep <i>(file)<i>"]
    end

    subgraph Parameters[<b>Parameters<b>]
      direction LR
      param1["_"]
    end

  end

  subgraph App[<b>CANTILEVER_SHEAR_APP<b>]
    direction RL
    proc["LabelingProc"]
  end

  subgraph Outputs[<b>OUTPUTS<b>]
    direction RL
    out2["labels.json <i>(file)<i>"]
  end

  Inputs --> proc
  proc --> Outputs

  classDef blueBox fill:#d0e6ff,stroke:#339,stroke-width:1.5px;
  class path1 blueBox;
```

```mermaid
flowchart LR
  subgraph Inputs[<b>INPUTS<b>]
    direction TB

    subgraph Paths[<b>Paths<b>]
      direction LR
      path1["mesh_settings.json <i>(file)<i>"]
      path2["labels.json <i>(file)<i>"]
    end

    subgraph Parameters[<b>Parameters<b>]
      direction LR
      param1["_"]
    end

  end

  subgraph App[<b>CANTILEVER_SHEAR_APP<b>]
    direction RL
    proc["MeshProc"]
  end

  subgraph Outputs[<b>OUTPUTS<b>]
    direction RL
    out3["mesh.msh <i>(file)<i>"]
  end

  Inputs --> proc
  proc --> Outputs

  classDef blueBox fill:#d0e6ff,stroke:#339,stroke-width:1.5px;
  class path2 blueBox;
```

```mermaid
flowchart LR
  subgraph Inputs[<b>INPUTS<b>]
    direction TB

    subgraph Paths[<b>Paths<b>]
      direction LR
      path1["mesh.msh <i>(file)<i>"]
    end

    subgraph Parameters[<b>Parameters<b>]
      direction LR
      param1["_"]
    end

  end

  subgraph App[<b>CANTILEVER_SHEAR_APP<b>]
    direction RL
    proc["ModelProc"]
  end

  subgraph Outputs[<b>OUTPUTS<b>]
    direction RL
    out3["model.vtk <i>(file)<i>"]
  end

  Inputs --> proc
  proc --> Outputs

  classDef blueBox fill:#d0e6ff,stroke:#339,stroke-width:1.5px;
  class path1 blueBox;
```

```mermaid
flowchart LR
  subgraph Inputs[<b>INPUTS<b>]
    direction TB

    subgraph Paths[<b>Paths<b>]
      direction LR
      path1["mesh_settings.json <i>(file)<i>"]
      path2["time_settings.json <i>(file)<i>"]
      path3["solver_settings.json <i>(file)<i>"]
      path4["mesh.msh <i>(file)<i>"]
      path5["model.vtk <i>(file)<i>"]
    end

    subgraph Parameters[<b>Parameters<b>]
      direction LR
      param1["mass"]
    end

  end

  subgraph App[<b>CANTILEVER_SHEAR_APP<b>]
    direction RL
    proc["SolverProc"]
  end

  subgraph Outputs[<b>OUTPUTS<b>]
    direction RL
    out1["solution <i>(folder)<i>"]
  end

  Inputs --> proc
  proc --> Outputs

  classDef blueBox fill:#d0e6ff,stroke:#339,stroke-width:1.5px;
  class path4 blueBox;
  class path5 blueBox;
```

```mermaid
flowchart LR
  subgraph Inputs[<b>INPUTS<b>]
    direction TB

    subgraph Paths[<b>Paths<b>]
      direction LR
      path1["model.vtk <i>(file)<i>"]
      path2["solution <i>(folder)<i>"]
    end

    subgraph Parameters[<b>Parameters<b>]
      direction LR
      param1["_"]
    end

  end

  subgraph App[<b>CANTILEVER_SHEAR_APP<b>]
    direction RL
    proc["PostProc"]
  end

  subgraph Outputs[<b>OUTPUTS<b>]
    direction RL
    out1["metrics.xlsx <i>(file)<i>"]
    out2["deflection.png <i>(file)<i>"]
  end

  Inputs --> proc
  proc --> Outputs

  classDef blueBox fill:#d0e6ff,stroke:#339,stroke-width:1.5px;
  class path1 blueBox;
  class path2 blueBox;
```

```mermaid
flowchart LR
  subgraph Inputs[<b>INPUTS<b>]
    direction TB

    subgraph Paths[<b>Paths<b>]
      direction LR
      path1["metrics.xlsx <i>(file)<i>"]
    end

    subgraph Parameters[<b>Parameters<b>]
      direction LR
      param1["_"]
    end

  end

  subgraph App[<b>CANTILEVER_SHEAR_APP<b>]
    direction RL
    proc["AnalysisProc"]
  end

  subgraph Outputs[<b>OUTPUTS<b>]
    direction RL
    out1["overall_comparisons.png <i>(file)<i>"]
    out2["overall_errors.csv <i>(file)<i>"]
  end

  Inputs --> proc
  proc --> Outputs

  classDef blueBox fill:#d0e6ff,stroke:#339,stroke-width:1.5px;
  class path1 blueBox;
```

### INPUTS

#### Parameters

- **`mass`:** Mass of the material.

#### Paths

- **`mesh_settings.json`:** File containing the mesh discretization settings.
- **`time_settings.json`:** File containing the time settings.
- **`solver_settings.json`:** File containing the solver settings.

### OUTPUTS

- **`geometry.brep`:** File containing the geometric model.
- **`labels.json`:** File containing the labeled geometric entities.
- **`mesh.msh`:** File containing the computational mesh (exported in Gmsh format).
- **`model.vtk`:** File containing the model object.
- **`solution`:** Directory containing the simulation results.
- **`metrics.xlsx`:** File containing the computed displacement metric.
- **`deflection.png`:** File containing the visual representation of the displacement metric.
- **`overall_comparisons.png`:** File containing the visual comparisons of the metrics for the various simulation runs.
- **`overall_errors.csv`:** File summarizing the obtained errors across all simulation runs.