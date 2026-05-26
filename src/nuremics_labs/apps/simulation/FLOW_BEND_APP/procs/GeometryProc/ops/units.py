import math

from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepBuilderAPI import (
    BRepBuilderAPI_MakeEdge,
    BRepBuilderAPI_MakeWire,
)
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipeShell
from OCC.Core.BRepTools import breptools
from OCC.Core.gp import gp_Ax2, gp_Circ, gp_Dir, gp_Pnt
from OCC.Core.TopAbs import TopAbs_VERTEX
from OCC.Core.TopExp import TopExp_Explorer


def create_geometry(
    r: float,
    R: float,
    L0: float,
    L1: float,
    outfile: str,
) -> None:
    
    ax2_circle = gp_Ax2(
        gp_Pnt(R, 0, 0),
        gp_Dir(0, -1, 0),
        gp_Dir(0, 0, 1),
    )
    circle = gp_Circ(ax2_circle, R)
    arc = BRepBuilderAPI_MakeEdge(circle, 0, math.pi / 2).Edge()

    pts = []
    exp = TopExp_Explorer(arc, TopAbs_VERTEX)
    while exp.More():
        v = exp.Current()
        pts.append(BRep_Tool.Pnt(v))
        exp.Next()

    P_start_ext = gp_Pnt(R + L0, 0, R)
    P_end_ext = gp_Pnt(0, 0, -L1)
    seg1 = BRepBuilderAPI_MakeEdge(P_start_ext, pts[0]).Edge()
    seg2 = BRepBuilderAPI_MakeEdge(pts[1], P_end_ext).Edge()
    
    wire = BRepBuilderAPI_MakeWire()
    wire.Add(seg1)
    wire.Add(arc)
    wire.Add(seg2)
    spine = wire.Wire()

    ax2_disk = gp_Ax2(P_start_ext, gp_Dir(1, 0, 0))  
    disk_circle = gp_Circ(ax2_disk, r)

    disk_edge = BRepBuilderAPI_MakeEdge(disk_circle).Edge()
    disk_wire = BRepBuilderAPI_MakeWire(disk_edge).Wire()

    pipe = BRepOffsetAPI_MakePipeShell(spine)
    pipe.Add(disk_wire)
    pipe.Build()
    pipe.MakeSolid()

    breptools.Write(pipe.Shape(), outfile)