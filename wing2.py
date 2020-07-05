from mh49 import mh49
from scale import scaleListOfTuple
from fattenTe import fattenTe
#from dumpAttr import dumpAttr
#from verticesAsList import verticesAsList

from pprint import pprint
import cadquery as cq # type: ignore

from typing import List, Sequence, Tuple

chord: float = 50
span: float = 20
tip: float = 5

# Normalize, Scale, fattenTe
scaleFactor: float = 1/mh49[0][0]
nMh49 = scaleListOfTuple(mh49, scaleFactor)
sMh49: List[Tuple[float, float]] = scaleListOfTuple(nMh49, chord)
fMh49: List[Tuple[float, float]] = fattenTe(sMh49, 0.75, 10)

h = 100
d = 25
X = 0
Y = 1
Z = 2

# Use "XY" with Jeremey's transformed(rotate) technique
xPos = (
    cq.Workplane("XY")
    .transformed(rotate=(0, 90, 0), offset=(0, 0, fMh49[-1][X]))
    #.polyline(fMh49).close()
    .spline(fMh49).close()
    .sweep(
        cq.Workplane("YX")
        # Start 0deg tangent, Tip finishes with 90deg tangent
        .spline([(0, i) for i in range(h-10)] + [(d-5,h+10)],[(0,1),(1,0)])

        # Start 0deg tangent, Tip finishes with 45deg tangent
        #.spline([(0,0),(0,h),(d,h+(5*d))],[(0,1),(1,1)]) #original
    )
)

wing2 = xPos.mirror("ZY").union(xPos)

#pprint(vars(result))
import io
tolerance=0.001;
f = io.open(f'wing2-direct-{tolerance}.stl', 'w+')
cq.exporters.exportShape(wing2, cq.exporters.ExportTypes.STL, f, tolerance)
f.close()

