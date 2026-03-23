"""
06 – Shell / Workplane-Selektoren
Zeigt: shell(), Workplane-Selektoren (">Z", "<Z", "#Z"),
       mehrere Workplanes in einer Kette.
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

# Shell: Quader aushohlen (Wandstaerke 0.2)
shell_box = (
    cq.Workplane("XY")
    .box(4, 3, 5)
    .faces(">Z")            # Deckelflaeche oeffnen
    .shell(-0.2)
)
save(shell_box, "06_shell")

# Workplane-Selektoren demonstrieren:
# Zylinder auf der Oberseite, Minus-Kugel auf der Unterseite
tower = (
    cq.Workplane("XY")
    .box(3, 3, 2)
    # Zylinder oben zentriert
    .faces(">Z").workplane()
    .cylinder(height=2, radius=0.6, combine=True)
    # Kugel von unten herausschneiden
    .faces("<Z").workplane(offset=-1)
    .sphere(1.2, combine="cut")
)
save(tower, "06_selectors")

print("06_shell_selectors: OK")
