# CANTILEVER_SHEAR_APP

<p align="left">
  <img src="https://img.shields.io/badge/pythonocc--core-7.4.0+-f7941e" />
  <img src="https://img.shields.io/badge/Gmsh-4.15.0+-ffffff" />
</p>

## Workflow

1. **[`GeometryProc`](https://github.com/nuremics/sim-labs/tree/cantilever-shear/src/nuremics_labs/apps/simulation/CANTILEVER_SHEAR_APP/procs/GeometryProc):** Create a geometric representation of a physical system.<br>
  A/ **`create_geometry`:** Create and export a simple geometric entity (1D line, 2D rectangle or 3D box) in BREP format.
2. **[`LabelingProc`](https://github.com/nuremics/sim-labs/tree/cantilever-shear/src/nuremics_labs/apps/simulation/CANTILEVER_SHEAR_APP/procs/LabelingProc):** Define and label the entities of a physical system from its geometric representation.<br>
  A/ **`label_entities`:** Assign labels to the entities of a geometric model.
3. **[`MeshProc`](https://github.com/nuremics/sim-labs/tree/cantilever-shear/src/nuremics_labs/apps/simulation/CANTILEVER_SHEAR_APP/procs/MeshProc):** Discretize the geometric representation of a physical system into a computational mesh and propagate defined labels onto the mesh entities.<br>
  A/ **`generate_mesh`:** Generate and export a computational mesh from a geometric model by discretizing the domain into mesh entities (nodes, elements) and assigning labeled physical groups.

```mermaid
flowchart RL
  Proc1[<b>GeometryProc<b>] e1@--1--o App[<b>CANTILEVER_SHEAR_APP<b>]
  Proc2[<b>LabelingProc<b>] e2@--2--o App
  Proc3[<b>MeshingProc<b>] e3@--3--o App
  Op11[<b>create_geometry<b>] e4@--A--o Proc1
  Op21[<b>label_entities<b>] e5@--A--o Proc2
  Op31[<b>generate_mesh<b>] e6@--A--o Proc3
  e1@{ animate: true }
  e2@{ animate: true }
  e3@{ animate: true }
  e4@{ animate: true }
  e5@{ animate: true }
  e6@{ animate: true }
```

## Mapping

```mermaid
erDiagram
  **CANTILEVER_SHEAR_APP** ||--|| **user_params** : mapping
  **CANTILEVER_SHEAR_APP** ||--|| **hard_params** : mapping
  **CANTILEVER_SHEAR_APP** ||--|| **output_paths** : mapping
  **user_params** ||--|| **GeometryProc** : mapping
  **hard_params** ||--|| **GeometryProc** : mapping
  **output_paths** ||--|| **GeometryProc** : mapping

  **user_params** {
    int dim "dimension"
  }
  **hard_params** {
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
  **CANTILEVER_SHEAR_APP** ||--|| **user_params** : mapping
  **CANTILEVER_SHEAR_APP** ||--|| **required_paths** : mapping
  **CANTILEVER_SHEAR_APP** ||--|| **output_paths** : mapping
  **user_params** ||--|| **LabelingProc** : mapping
  **required_paths** ||--|| **LabelingProc** : mapping
  **output_paths** ||--|| **LabelingProc** : mapping

  **user_params** {
    int dim "dimension"
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
  **CANTILEVER_SHEAR_APP** ||--|| **user_params** : mapping
  **CANTILEVER_SHEAR_APP** ||--|| **user_paths** : mapping
  **CANTILEVER_SHEAR_APP** ||--|| **required_paths** : mapping
  **CANTILEVER_SHEAR_APP** ||--|| **output_paths** : mapping
  **user_params** ||--|| **MeshProc** : mapping
  **user_paths** ||--|| **MeshProc** : mapping
  **required_paths** ||--|| **MeshProc** : mapping
  **output_paths** ||--|| **MeshProc** : mapping

  **user_params** {
    int dim "dimension"
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
      param1["dimension <i>(int)<i>"]
    end
  end

  subgraph App[<b>CANTILEVER_SHEAR_APP<b>]
    direction RL
    proc1["GeometryProc"]
    proc2["LabelingProc"]
    proc3["MeshProc"]
  end

  subgraph Outputs[<b>OUTPUTS<b>]
    direction RL
    out1["geometry.brep <i>(file)<i>"]
    out2["labels.json <i>(file)<i>"]
    out3["mesh.msh <i>(file)<i>"]
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
      param1["dimension <i>(int)<i>"]
    end
  end

  subgraph App[<b>CANTILEVER_SHEAR_APP<b>]
    direction RL
    proc1["GeometryProc"]
  end

  subgraph Outputs[<b>OUTPUTS<b>]
    direction RL
    out1["geometry.brep <i>(file)<i>"]
  end

  Inputs --> proc1
  proc1 --> Outputs
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
      param1["dimension <i>(int)<i>"]
    end

  end

  subgraph App[<b>CANTILEVER_SHEAR_APP<b>]
    direction RL
    proc2["LabelingProc"]
  end

  subgraph Outputs[<b>OUTPUTS<b>]
    direction RL
    out2["labels.json <i>(file)<i>"]
  end

  Inputs --> proc2
  proc2 --> Outputs

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
      param1["dimension <i>(int)<i>"]
    end

  end

  subgraph App[<b>CANTILEVER_SHEAR_APP<b>]
    direction RL
    proc2["MeshProc"]
  end

  subgraph Outputs[<b>OUTPUTS<b>]
    direction RL
    out3["mesh.msh <i>(file)<i>"]
  end

  Inputs --> proc2
  proc2 --> Outputs

  classDef blueBox fill:#d0e6ff,stroke:#339,stroke-width:1.5px;
  class path1 blueBox;
```

### INPUTS

#### Parameters

- **`dimension`:** Dimension of the geometry (`1` for a 1D line, `2` for a 2D rectangle, `3` for a 3D box).

#### Paths

- **`mesh_settings.json`:** File containing the mesh discretization settings.

### OUTPUTS

- **`geometry.brep`:** File containing the geometric model.
- **`labels.json`:** File containing the labeled geometric entities.
- **`mesh.msh`:** File containing the output mesh (exported in Gmsh format).