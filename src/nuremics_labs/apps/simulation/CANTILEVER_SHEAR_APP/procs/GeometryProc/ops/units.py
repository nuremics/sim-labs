import sys

from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeWire
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepTools import breptools
from OCC.Core.TopoDS import TopoDS_Shape


def create_geometry(
    dim: int,
    length: float,
    width: float,
    height: float,
    outfile: str,
):
    """
    Create and export a simple geometric entity (3D plate, 2D shell, or 1D beam)
    in BREP format.

    Depending on the specified dimension, this function generates:
    - A 3D rectangular block (plate)
    - A 2D rectangular surface (shell)
    - A 1D line (beam)

    Parameters
    ----------
    dim : int
        Dimension of the geometry: 
        1 for a line (beam), 2 for a rectangle (plate), 3 for a box (block).
    length : float
        Length of the geometry along the X axis.
    width : float
        Width of the geometry along the Y axis (only used if dim = 2/3).
    height : float
        Height of the geometry along the Z axis (only used if dim = 3).
    outfile : str
        Name of the output file where the created geometry will be saved.
    """

    if dim == 3:
        shape = _create_plate(
            length=length,
            width=width,
            height=height,
        )
    elif dim == 2:
        shape = _create_shell(
            length=length,
            width=width,
        )
    elif dim == 1:
        shape = _create_beam(
            length=length,
        )
    else:
        sys.exit("Dimension must be either 1, 2 or 3.")

    breptools.Write(shape, outfile)


def _create_plate(
    length: float,
    width: float,
    height: float,
) -> TopoDS_Shape:

    origin = gp_Pnt(0.0, -width / 2.0, -height / 2.0)
    shape = BRepPrimAPI_MakeBox(origin, length, width, height).Shape()

    return shape


def _create_shell(
    length: float,
    width: float,
) -> TopoDS_Shape:

    x0, y0 = 0.0, -width / 2.0
    x1, y1 = x0 + length, y0 + width

    p1 = gp_Pnt(x0, y0, 0)
    p2 = gp_Pnt(x1, y0, 0)
    p3 = gp_Pnt(x1, y1, 0)
    p4 = gp_Pnt(x0, y1, 0)

    e1 = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
    e2 = BRepBuilderAPI_MakeEdge(p2, p3).Edge()
    e3 = BRepBuilderAPI_MakeEdge(p3, p4).Edge()
    e4 = BRepBuilderAPI_MakeEdge(p4, p1).Edge()

    wire_maker = BRepBuilderAPI_MakeWire()
    for e in [e1, e2, e3, e4]:
        wire_maker.Add(e)
    wire = wire_maker.Wire()

    shape = BRepBuilderAPI_MakeFace(wire).Face()

    return shape


def _create_beam(
    length: float,
) -> TopoDS_Shape:

    p0 = gp_Pnt(0, 0, 0)
    p1 = gp_Pnt(length, 0, 0)

    edge = BRepBuilderAPI_MakeEdge(p0, p1).Edge()
    shape = BRepBuilderAPI_MakeWire(edge).Wire()

    return shape