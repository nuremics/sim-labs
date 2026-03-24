# CANTILEVER_SHEAR_APP

<p align="left">
  <img src="https://img.shields.io/badge/pythonocc--core-7.4.0+-f7941e" />
  <img src="https://img.shields.io/badge/Gmsh-4.15.0+-ffffff" />
  <img src="https://img.shields.io/badge/meshio-5.3.5+-81ecec" />
  <img src="https://img.shields.io/badge/NumPy-2.4.2+-4dabcf?style=flat&logo=numpy&logoColor=white" />
  <img src="https://img.shields.io/badge/PyVista-0.47.1+-00b25e" />
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

```mermaid
flowchart RL
  Proc1[<b>GeometryProc<b>] e1@--1--o App[<b>CANTILEVER_SHEAR_APP<b>]
  Proc2[<b>LabelingProc<b>] e2@--2--o App
  Proc3[<b>MeshingProc<b>] e3@--3--o App
  Proc4[<b>ModelProc<b>] e4@--4--o App
  Op11[<b>create_geometry<b>] e5@--A--o Proc1
  Op21[<b>label_entities<b>] e6@--A--o Proc2
  Op31[<b>generate_mesh<b>] e7@--A--o Proc3
  Op41[<b>build_model<b>] e8@--A--o Proc4
  e1@{ animate: true }
  e2@{ animate: true }
  e3@{ animate: true }
  e4@{ animate: true }
  e5@{ animate: true }
  e6@{ animate: true }
  e7@{ animate: true }
  e8@{ animate: true }
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

## I/O Interface

```mermaid
flowchart LR
  subgraph Inputs[<b>INPUTS<b>]
    direction TB

    subgraph Paths[<b>Paths<b>]
      direction LR
      path["mesh_settings.json <i>(file)<i>"]
    end

    subgraph Parameters[<b>Parameters<b>]
      direction LR
      param1["_"]
    end
  end

  subgraph App[<b>CANTILEVER_SHEAR_APP<b>]
    direction RL
    proc1["GeometryProc"]
    proc2["LabelingProc"]
    proc3["MeshProc"]
    proc4["ModelProc"]
  end

  subgraph Outputs[<b>OUTPUTS<b>]
    direction RL
    out1["geometry.brep <i>(file)<i>"]
    out2["labels.json <i>(file)<i>"]
    out3["mesh.msh <i>(file)<i>"]
    out3["model.vtk <i>(file)<i>"]
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
      path1["labels.json <i>(file)<i>"]
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
  class path1 blueBox;
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

### INPUTS

#### Parameters

NA

<!-- - **`dimension`:** Dimension of the geometry (`1` for a 1D line, `2` for a 2D rectangle, `3` for a 3D box). -->

#### Paths

- **`mesh_settings.json`:** File containing the mesh discretization settings.

### OUTPUTS

- **`geometry.brep`:** File containing the geometric model.
- **`labels.json`:** File containing the labeled geometric entities.
- **`mesh.msh`:** File containing the computational mesh (exported in Gmsh format).
- **`model.vtk`:** File containing the model object.