# SolverProc

<p align="left">
  <img src="https://img.shields.io/badge/SOFA Framework-25.6.0-e84e1c" />
  <img src="https://img.shields.io/badge/NumPy-2.4.2+-4dabcf?style=flat&logo=numpy&logoColor=white" />
  <img src="https://img.shields.io/badge/PyVista-0.48.0+-00b25e" />
  <img src="https://img.shields.io/badge/imageio-2.37.0+-000000" />
</p>

## Process

Compute the mechanical deformation of a physical system under prescribed boundary conditions.<br>
A/ **`run_solver`:** Define the simulation setup, apply boundary conditions, and execute the solver to compute the raw simulation results.<br>
B/ **`compile_solution`:** Compile the raw simulation results into a PVD format and compute the displacement field over the model.<br>
C/ **`create_animation`:** Create an animation of the simulation results.

```mermaid
erDiagram
  **Parameters** ||--|| **Inputs** : provides
  **Paths** ||--|| **Inputs** : provides
  **Inputs** ||--|| **ModelProc** : feeds
  **ModelProc** ||--|| **Outputs** : generates

  **Parameters** {
    mass float
    young float
    poisson float
    force float
  }
  **Paths** {
    file mesh_settings_file "json"
    file time_settings_file "json"
    file solver_settings_file "json"
    file mesh_file "msh"
    file model_file "vtk"
  }
  **ModelProc** {
    op run_solver
    op compile_solution
    op create_animation
  }
  **Outputs** {
    folder outdir "_"
  }
```

## Input Parameter(s)

- **`mass`:** Mass of the material.
- **`young`:** Young's modulus of the material. 
- **`poisson`:** Poisson's ratio of the material.
- **`force`:** Magnitude of the external force applied to the system as a boundary condition.

## Input Path(s)

- **`mesh_settings_file`:** File containing the mesh discretization settings.
- **`time_settings_file`:** File containing the time settings.
- **`solver_settings_file`:** File containing the solver settings.
- **`mesh_file`:** File containing the meshed geometry and physical group definitions (in Gmsh format).
- **`model_file`:** File containing the model object.

## Output Path(s)

- **`outdir`:** Directory containing the simulation results.