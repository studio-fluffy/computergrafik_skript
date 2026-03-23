"""
05 – Fasen, Abrundungen, Bohrungen
Zeigt: chamfer(), fillet(), cboreHole(), hole()
Export: STEP (3D) + SVG (Konstruktionsansicht)
"""
import cadquery as cq
from pathlib import Path

out = Path(__file__).parent


def save(shape, name):
    cq.exporters.export(shape, str(out / f"{name}.step"))
    cq.exporters.export(shape, str(out / f"{name}.svg"),
                        opt={"width": 400, "height": 300,
                             "marginLeft": 20, "marginTop": 20,
                             "showAxes": True, "projectionDir": (1, 1, 0.5),
                             "showHidden": False})
    print(f"  {name}.step + .svg")

# Fase an jeder Kante der Oberflaeche
chamfered = (
    cq.Workplane("XY")
    .box(4, 4, 2)
    .edges("|Z")        # alle vertikalen Kanten
    .chamfer(0.3)
)
save(chamfered, "05_chamfer")

# Rundung an oben/unten
filleted = (
    cq.Workplane("XY")
    .box(4, 4, 2)
    .edges("#Z")        # horizontale Ober-/Unterkanten
    .fillet(0.4)
)
save(filleted, "05_fillet")

# Schraubenbohrungen  (4x im Raster)
plate_with_holes = (
    cq.Workplane("XY")
    .box(6, 6, 1)
    .faces(">Z")
    .workplane()
    .rect(4, 4, forConstruction=True)
    .vertices()
    .cboreHole(diameter=0.5, cboreDiameter=1.0, cboreDepth=0.4)
)
save(plate_with_holes, "05_holes")

print("05_chamfer_fillet_holes: OK")
