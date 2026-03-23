"""
02 – Transformationen
Zeigt: translate(), rotate(), mirror()
Drei Kugeln werden angeordnet und gespiegelt.
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

result = (
    cq.Workplane("XY")
    # Kugel in der Mitte
    .sphere(0.5)
    # Zweite Kugel nach rechts verschoben
    .union(cq.Workplane("XY").sphere(0.5).translate((3, 0, 0)))
    # Dritte Kugel um 45° gedreht und nach oben versetzt
    .union(
        cq.Workplane("XY")
        .cylinder(height=2, radius=0.3)
        .rotate((0, 0, 0), (0, 1, 0), 45)
        .translate((6, 0, 1))
    )
)

save(result, "02_transforms")
print("02_transforms: OK")
