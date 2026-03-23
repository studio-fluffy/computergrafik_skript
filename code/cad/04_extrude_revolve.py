"""
04 – 2D-Profil -> Extrusion & Revolution
Zeigt: rect(), circle(), extrude(), revolve()
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

# L-Profil extrudieren
l_profile = (
    cq.Workplane("XY")
    .polyline([(0, 0), (0, 4), (1, 4), (1, 1), (3, 1), (3, 0)])
    .close()
    .extrude(8)
)
save(l_profile, "04_extrude")

# Kreis um die Z-Achse revolvieren -> Torus-aehnlich
torus = (
    cq.Workplane("XZ")
    .center(3, 0)          # Offset von der Drehachse
    .circle(0.5)
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
save(torus, "04_revolve")

print("04_extrude_revolve: OK")
