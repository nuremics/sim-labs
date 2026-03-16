# CANTILEVER_SHEAR_APP

<p align="left">
  <img src="https://img.shields.io/badge/pythonocc--core-7.4.0+-f7941e" />
</p>

## Workflow

1. **[`GeometryProc`](https://github.com/nuremics/sim-labs/tree/cantilever-shear/src/nuremics_labs/apps/simulation/CANTILEVER_SHEAR_APP/procs/GeometryProc):** Create a geometric representation of a physical system.<br>
  A/ **`create_geometry`:** Create and export a simple geometric entity (3D solid, 2D shell or 1D beam) in BREP format.
2. **[`LabelingProc`](https://github.com/nuremics/sim-labs/tree/cantilever-shear/src/nuremics_labs/apps/simulation/CANTILEVER_SHEAR_APP/procs/LabelingProc):** Define and label the entities of a physical system from its geometric representation.<br>
  A/ **`label_entities`:** Assign labels to the entities of a geometric model.

```mermaid
flowchart RL
  **GeometryProc** e1@--1--o **CANTILEVER_SHEAR_APP**
  **LabelingProc** e2@--2--o **CANTILEVER_SHEAR_APP**
  **create_geometry** e3@--A--o **GeometryProc**
  **label_entities** e4@--A--o **LabelingProc**
  e1@{ animate: true }
  e2@{ animate: true }
  e3@{ animate: true }
  e4@{ animate: true }
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

## I/O Interface

```mermaid
flowchart LR
  subgraph **INPUTS**
    direction TB

    subgraph **Paths**
      direction LR
      path["_"]
    end

    subgraph **Parameters**
      direction LR
      param1["dimension _(int)_"]
    end
  end

  subgraph **CANTILEVER_SHEAR_APP**
    direction RL
    proc1["GeometryProc"]
    proc2["LabelingProc"]
  end

  subgraph **OUTPUTS**
    direction RL
    out1["geometry.brep _(file)_"]
    out2["labels.json _(file)_"]
  end

  **INPUTS** --> **CANTILEVER_SHEAR_APP**
  **CANTILEVER_SHEAR_APP** --> **OUTPUTS**
```

```mermaid
flowchart LR
  subgraph **INPUTS**
    direction TB

    subgraph **Paths**
      direction LR
      path["_"]
    end

    subgraph **Parameters**
      direction LR
      param1["dimension _(int)_"]
    end
  end

  subgraph **CANTILEVER_SHEAR_APP**
    direction RL
    proc1["GeometryProc"]
  end

  subgraph **OUTPUTS**
    direction RL
    out1["geometry.brep _(file)_"]
  end

  **INPUTS** --> proc1
  proc1 --> **OUTPUTS**
```

```mermaid
flowchart LR
  subgraph **INPUTS**
    direction TB

    subgraph **Paths**
      direction LR
      out1["geometry.brep _(file)_"]
    end

    subgraph **Parameters**
      direction LR
      param1["dimension _(int)_"]
    end

  end

  subgraph **CANTILEVER_SHEAR_APP**
    direction RL
    proc2["LabelingProc"]
  end

  subgraph **OUTPUTS**
    direction RL
    out2["labels.json _(file)_"]
  end

  **INPUTS** --> proc2
  proc2 --> **OUTPUTS**

  classDef blueBox fill:#d0e6ff,stroke:#339,stroke-width:1.5px;
  class out1 blueBox;
```

### INPUTS

#### Parameters

- **`dimension`:** Dimension of the geometry: 1 for a 1D line (beam), 2 for a 2D surface (shell), 3 for a 3D volume (solid).

#### Paths

N/A

### OUTPUTS

- **`geometry.brep`:** File containing the geometric model.
- **`labels.json`:** File containing the labeled geometric entities.