# LabelingProc

## Process

Define and label the entities of a physical system from its geometric representation.<br>
A/ **`label_entities`:** Assign labels to the entities of a geometric model.

```mermaid
erDiagram
  **Parameters** ||--|| **Inputs** : provides
  **Paths** ||--|| **Inputs** : provides
  **Inputs** ||--|| **LabelingProc** : feeds
  **LabelingProc** ||--|| **Outputs** : generates

  **Parameters** {
    int dim
  }
  **Paths** {
    file infile "brep"
  }
  **LabelingProc** {
    op label_entities
  }
  **Outputs** {
    file outfile "json"
  }
```

## Input Parameter(s)

- **`dim`:** Dimension of the geometry: 1 for a 1D line (beam), 2 for a 2D surface (plate), 3 for a 3D volume (solid).

## Input Path(s)

- **`infile`:** File containing the geometric model.

## Output Path(s)

- **`outfile`:** File containing the labeled geometric entities.