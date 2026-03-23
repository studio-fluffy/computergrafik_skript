"""
01 – Primitive Grundkoerper
Zeigt: box(), sphere(), cylinder()
Export: STEP (3D) + SVG (Konstruktionsansicht)
"""
import cadquery as cq
from pathlib import Path

out = Path(__file__).parent


def save(shape, name):
    """Speichert STEP und SVG nebeneinander."""
    cq.exporters.export(shape, str(out / f"{name}.step"))
    cq.exporters.export(shape, str(out / f"{name}.svg"),
                        opt={"width": 400, "height": 300,
                             "marginLeft": 20, "marginTop": 20,
                             "showAxes": True, "projectionDir": (1, 1, 0.5),
                             "showHidden": False})
    print(f"  {name}.step + .svg")


# Quader  1 x 2 x 3
save(cq.Workplane("XY").box(1, 2, 3), "01_box")

# Kugel  r = 1
save(cq.Workplane("XY").sphere(1), "01_sphere")

# Zylinder  r = 0.5, h = 2
save(cq.Workplane("XY").cylinder(height=2, radius=0.5), "01_cylinder")

print("01_primitives: OK")
