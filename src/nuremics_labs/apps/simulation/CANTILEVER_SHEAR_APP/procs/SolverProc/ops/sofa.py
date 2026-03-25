import os

import numpy as np
import pandas as pd
import pyvista as pv
import Sofa
import Sofa.Gui
import SofaImGui  # noqa: F401


def main(
    mesh_file: str,
    model_file: str,
    young: float,
    poisson: float,
    mass: float,
    elem: str,
    ramp: float,
    final_time: float,
    dt: float,
    force: float,
    scheme: str,
    solver: str,
    dump_path: str,
    silent: bool,
) -> None:
    
    # Define number of steps
    nb_step = int(final_time / dt)

    # Define export frequency
    nb_dump = 100
    every_n_step = int(nb_step / nb_dump)
    if every_n_step == 0:
        every_n_step = 1

    # Call the SOFA function to create the root node
    root = Sofa.Core.Node("root")

    # Call the createScene function, as runSofa does
    createScene(
        root=root,
        mesh_file=mesh_file,
        model_file=model_file,
        mass=mass,
        young=young,
        poisson=poisson,
        force=force,
        elem=elem,
        ramp=ramp,
        dt=dt,
        every_n_step=every_n_step,
        scheme=scheme,
        solver=solver,
        dump_path=dump_path,
    )

    # Once defined, initialization of the scene graph
    Sofa.Simulation.initRoot(root)

    if not silent:

        # Launch the GUI
        Sofa.Gui.GUIManager.Init("myscene", "imgui")
        Sofa.Gui.GUIManager.createGUI(root, __file__)
        Sofa.Gui.GUIManager.SetDimension(1080, 800)

        # Initialization of the scene will be done here
        Sofa.Gui.GUIManager.MainLoop(root)
        Sofa.Gui.GUIManager.closeGUI()
    
    else:

        # Define simulation loop
        for _ in range(nb_step):
            Sofa.Simulation.animate(root, root.dt.value)


def createScene(
    root: Sofa.Core.Node,
    mesh_file: str,
    model_file: str,
    young: float,
    poisson: float,
    mass: float,
    elem: str,
    ramp: float,
    dt: float,
    every_n_step: int,
    force: float,
    scheme: str,
    solver: str,
    dump_path: str,
) -> None:

    mesh = pv.read(model_file)

    mask = mesh.point_data["Constraint"] == 1
    ids_constraint = np.where(mask)[0].tolist()

    mask = mesh.point_data["Load"] == 1
    ids_load = np.where(mask)[0].tolist()

    root.gravity = [0.0, 0.0, 0.0]
    root.dt = dt

    root.addObject("RequiredPlugin", name="Sofa.Component.AnimationLoop")
    root.addObject("RequiredPlugin", name="Sofa.Component.Collision.Detection.Algorithm")
    root.addObject("RequiredPlugin", name="Sofa.Component.Collision.Detection.Intersection")
    root.addObject("RequiredPlugin", name="Sofa.Component.Collision.Geometry")
    root.addObject("RequiredPlugin", name="Sofa.Component.Collision.Response.Contact")
    root.addObject("RequiredPlugin", name="Sofa.Component.Constraint.Lagrangian.Correction")
    root.addObject("RequiredPlugin", name="Sofa.Component.Constraint.Lagrangian.Solver")
    root.addObject("RequiredPlugin", name="Sofa.Component.Constraint.Projective")
    root.addObject("RequiredPlugin", name="Sofa.Component.IO.Mesh")
    root.addObject("RequiredPlugin", name="Sofa.Component.LinearSolver.Direct")
    root.addObject("RequiredPlugin", name="Sofa.Component.ODESolver.Backward")
    root.addObject("RequiredPlugin", name="Sofa.Component.SolidMechanics.FEM.Elastic")
    root.addObject("RequiredPlugin", name="Sofa.Component.MechanicalLoad")
    root.addObject("RequiredPlugin", name="Sofa.Component.StateContainer")
    root.addObject("RequiredPlugin", name="Sofa.Component.Mass")
    root.addObject("RequiredPlugin", name="Sofa.Component.Topology.Container.Constant")
    root.addObject("RequiredPlugin", name="Sofa.Component.Topology.Container.Dynamic")
    root.addObject("RequiredPlugin", name="Sofa.Component.Visual")
    root.addObject("RequiredPlugin", name="Sofa.Component.ODESolver.Forward")
    root.addObject("RequiredPlugin", name="Sofa.GL.Component.Rendering3D")
    root.addObject("RequiredPlugin", name="Sofa.Component.LinearSolver.Preconditioner")
    
    root.addObject("VisualStyle",
        displayFlags=[
            "hideVisualModels",
            "hideBehaviorModels",
            "showMappings",
            "showForceFields"
        ]
    )
    
    root.addObject("DefaultAnimationLoop")

    if mass == 0.0:
        root.addObject("StaticSolver",
            newton_iterations=10,
            absolute_correction_tolerance_threshold=1.0e-20,
            absolute_residual_tolerance_threshold=1.0e-20,
            should_diverge_when_residual_is_growing=True,
        )
    else:
        if scheme == "backward":
            root.addObject("EulerImplicitSolver",
                name="odesolver",
                rayleighStiffness=0.3,
                rayleighMass=0.0,
            )
        elif scheme == "forward":
            root.addObject("RungeKutta4Solver",
                name="odesolver",
            )

    if solver == "direct":
        root.addObject("SparseLDLSolver",
            name="linear solver",
            template="CompressedRowSparseMatrixMat3x3d",
        )
    elif solver == "iterative":
        root.addObject("CGLinearSolver",
            name="linear solver",
            iterations=5000,
            tolerance=1e-6,
            threshold=1e-6,
        )
    
    body = root.addChild("plate")
    body.addObject("MeshTopology",
        name="mesh",
        filename=mesh_file,
    )
    body.addObject("MeshGmshLoader",
        name="loader",
        filename=mesh_file,
    )
    body.addObject("MechanicalObject",
        template="Vec3",
        name="dofs",
        src="@loader",
    )
    if (elem == "tetra") or (elem == "utetra"):
        body.addObject("TetrahedronFEMForceField",
            template="Vec3",
            name="FEM",
            youngModulus=young,
            poissonRatio=poisson,
            method="large",
        )
    elif elem == "hexa":
        body.addObject("HexahedronFEMForceField",
            template="Vec3",
            name="FEM",
            youngModulus=young,
            poissonRatio=poisson,
            method="large",
        )
    if mass != 0.0:
        body.addObject("MeshMatrixMass",
            name="mass",
            totalMass=mass,
            topology="@mesh",
        )
    body.addObject("FixedConstraint",
        name="FixedConstraint",
        indices=ids_constraint,
    )
    body.addObject("ConstantForceField",
        name="Load",
        indices=ids_load,
        totalForce=[0.0, 0.0, 0.0],
        showArrowSize=10.0,
    )
    body.addObject(
        TimeDependentLoad(
            node=body,
            dt=dt,
            ramp=ramp,
            every_n_step=every_n_step,
            force=force,
        )
    )
    body.addObject("VTKExporter",
        filename=os.path.join(dump_path, "solution"),
        listening="true",
        edges=0,
        triangles=0,
        quads=0,
        tetras=1,
        hexas=1,
        exportEveryNumberOfSteps=every_n_step,
        exportAtBegin=False,
        exportAtEnd=True,
    )

    return root


class TimeDependentLoad(Sofa.Core.Controller):

    def __init__(self, *args: object, **kwargs: object) -> None:
        
        Sofa.Core.Controller.__init__(self, *args, **kwargs)
        
        self.node = kwargs.get("node")
        self.load = self.node.getObject("Load")

        self.dt = kwargs.get("dt")
        self.ramp = kwargs.get("ramp")
        self.every_n_step = kwargs.get("every_n_step")
        self.force = kwargs.get("force")

        self.df_force_record = pd.DataFrame(
            columns=["Time", "Force"]
        )
        self.dump_id = 0 

    def onAnimateBeginEvent(self, event: object) -> None:
        
        current_time = self.node.time.value
        self.updateLoad(current_time)

    def updateLoad(self, current_time: float) -> None:
        
        if current_time <= self.ramp:
            self.load.totalForce = [0.0, 0.0, self.force * current_time / self.ramp]
        else:
            self.load.totalForce = [0.0, 0.0, self.force]

        step_id = int(0.5 + current_time / self.dt)
        if step_id >= self.dump_id:

            new_row = {"Time": current_time, "Force": self.load.totalForce.value[2]}
            self.df_force_record.loc[len(self.df_force_record)] = new_row
            self.df_force_record.to_excel("force_record.xlsx", index=False)

            self.dump_id += self.every_n_step


if __name__ == '__main__':

    mesh_file = r"..."
    model_file = r"..."
    results_path = r"..."
    young = 1.2e6
    poisson = 0.0
    mass = 5.0
    dt = 1.0
    ramp = 100.0
    force = 4.0
    elem = "hexa"
    scheme = "backward"
    solver = "direct"
    
    main(
        mesh_file=mesh_file,
        model_file=model_file,
        young=young,
        poisson=poisson,
        mass=mass,
        elem=elem,
        dt=dt,
        ramp=ramp,
        force=force,
        scheme=scheme,
        solver=solver,
        results_path=results_path,
        silent=False,
    )