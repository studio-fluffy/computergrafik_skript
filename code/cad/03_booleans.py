"""
03 – Boolesche Operationen
Zeigt: union(), cut(), intersect()
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

box    = cq.Workplane("XY").box(2, 2, 2)
sphere = cq.Workplane("XY").sphere(1.3)

# Union: Box + Kugel zusammengefuegt
save(box.union(sphere), "03_union")

# Cut: Kugel aus Box herausgeschnitten
save(cq.Workplane("XY").box(2, 2, 2).cut(sphere), "03_cut")

# Intersect: Schnittmenge
save(cq.Workplane("XY").box(2, 2, 2).intersect(sphere), "03_intersect")

print("03_booleans: OK")
