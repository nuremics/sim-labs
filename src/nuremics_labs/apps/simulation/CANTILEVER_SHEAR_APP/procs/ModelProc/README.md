# ModelProc

<p align="left">
  <img src="https://img.shields.io/badge/meshio-5.3.5+-81ecec" />
  <img src="https://img.shields.io/badge/NumPy-2.4.2+-4dabcf?style=flat&logo=numpy&logoColor=white" />
  <img src="https://img.shields.io/badge/PyVista-0.47.1+-00b25e" />
</p>

## Process

Convert a meshed geometry into a model object mapping geometric labels to mesh entities.<br>
A/ **`build_model`:** Build a VTK-based model object from a meshed geometry by creating data fields that map physical groups to their corresponding nodes and elements.

```mermaid
erDiagram
  **Parameters** ||--|| **Inputs** : provides
  **Paths** ||--|| **Inputs** : provides
  **Inputs** ||--|| **ModelProc** : feeds
  **ModelProc** ||--|| **Outputs** : generates

  **Parameters** {
    _ _
  }
  **Paths** {
    file infile "msh"
  }
  **ModelProc** {
    op build_model
  }
  **Outputs** {
    file outfile "vtk"
  }
```

## Input Parameter(s)

NA

## Input Path(s)

- **`infile`:** File containing the meshed geometry and physical group definitions (in Gmsh format).

## Output Path(s)

- **`outfile`:** File containing the model object.