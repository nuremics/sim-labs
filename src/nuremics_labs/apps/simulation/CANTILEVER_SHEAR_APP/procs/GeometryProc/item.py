import os
import attrs
from pathlib import Path

from nuremics import Process
from nuremics_labs.apps.simulation.CANTILEVER_SHEAR_APP.procs.GeometryProc.ops import (
    create_geometry,
)


@attrs.define
class GeometryProc(Process):
    """
    Create a geometric representation of a physical system.

    Process
    -------
        A/ create_geometry
            Create and export a simple geometric entity (1D line, 2D rectangle or 3D box)
            in BREP format.

    Input parameters
    ----------------
        dim : int
            Dimension of the geometry: 
            - 1 for a 1D line (beam)
            - 2 for a 2D rectangle (shell)
            - 3 for a 3D box (solid)
        length : float
            Length of the geometry along the X axis.
        width : float
            Width of the geometry along the Y axis (only used if dim = 2|3).
        height : float
            Height of the geometry along the Z axis (only used if dim = 3).

    Outputs
    -------
        outfile : .brep
            File containing the geometric model.
    """

    # Parameters
    dim: int = attrs.field(init=False, metadata={"input": True})
    length: float = attrs.field(init=False, metadata={"input": True})
    width: float = attrs.field(init=False, metadata={"input": True})
    height: float = attrs.field(init=False, metadata={"input": True})

    # Outputs
    outfile: Path = attrs.field(init=False, metadata={"output": True}, converter=Path)

    def __call__(self):
        super().__call__()

        self.create_geometry()

    def create_geometry(self):
        """
        Create and export a simple geometric entity (1D line, 2D rectangle or 3D box)
        in BREP format.

        Uses
        ----
            dim
            length
            width
            height
        
        Generates
        ---------
            outfile
        """

        create_geometry(
            dim=self.dim,
            length=self.length,
            width=self.width,
            height=self.height,
            outfile=str(self.outfile),
        )


if __name__ == "__main__":

    # ================================================================== #
    #                      USER-DEFINED PARAMETERS                       #
    #              >>>>> TO BE EDITED BY THE OPERATOR <<<<<              #
    # ================================================================== #

    # Working directory
    working_dir = Path(r"...")

    # Input parameters
    dim = 3
    length = 10.0 
    width = 1.0
    height = 0.1

    # Output paths
    outfile = "geometry.brep"

    # ================================================================== #

    # Go to working directory
    os.chdir(working_dir)

    # Create dictionary containing input data
    dict_inputs = {
        "dim": dim,
        "length": length,
        "width": width,
        "height": height,
    }

    # Create process
    process = GeometryProc(
        dict_inputs=dict_inputs,
        set_inputs=True,
    )

    # Define output paths
    process.output_paths["outfile"] = outfile

    # Run process
    process()
    process.finalize()