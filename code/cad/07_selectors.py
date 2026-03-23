"""
07 – Selektoren

Selektoren sind der Kern von CadQuery: Sie erlauben es, gezielt Faces (Flaechen),
Edges (Kanten) oder Vertices (Punkte) eines Koerpers anzusprechen, ohne deren
genaue Koordinaten kennen zu muessen.

Systematik:
  ">Achse"   – die Flaeche/Kante, die am weitesten in +Achse-Richtung liegt
  "<Achse"   – das Gegenteil (negativste)
  "|Achse"   – parallel zur Achse  (z.B. alle vertikalen Kanten)
  "#Achse"   – senkrecht zur Achse (z.B. alle horizontalen Kanten)
  "+Achse"   – zeigt in +Achse Richtung (Normalenvektor)
  "%Form"    – geometrischer Typ: PLANE, CYLINDER, SPHERE, CONE, TORUS, ...

  Logische Kombinatoren:
  "A and B"  – beide Bedingungen erfuellt
  "A or B"   – mindestens eine erfuellt
  "not A"    – Negation

Export: STEP + SVG zur Konstruktionsansicht
"""
import cadquery as cq
from pathlib import Path

out = Path(__file__).parent


def save(shape, name):
    cq.exporters.export(shape, str(out / f"{name}.step"))
    cq.exporters.export(shape, str(out / f"{name}.svg"),
                        opt={"width": 500, "height": 400,
                             "marginLeft": 20, "marginTop": 20,
                             "showAxes": True, "projectionDir": (1, 1, 0.5),
                             "showHidden": False})
    print(f"  {name}.step + .svg")


# ─────────────────────────────────────────────────────────────────────────────
# 1) >Z / <Z – hoechtse und niedrigste Flaeche
#    Deckelflaeche bekommt eine zentrale Bohrung,
#    Bodenflaeche bekommt eine Senkung.
# ─────────────────────────────────────────────────────────────────────────────
top_bottom = (
    cq.Workplane("XY")
    .box(4, 4, 3)
    # Bohrung von oben
    .faces(">Z").workplane()
    .hole(diameter=1.0, depth=2.0)
    # Fase auf der untersten Flaeche
    .faces("<Z").edges()
    .chamfer(0.2)
)
save(top_bottom, "07a_top_bottom")

# ─────────────────────────────────────────────────────────────────────────────
# 2) |Z – alle Kanten parallel zur Z-Achse (= vertikale Kanten)
#    Alle vier vertikalen Kanten werden abgerundet.
# ─────────────────────────────────────────────────────────────────────────────
vertical_fillet = (
    cq.Workplane("XY")
    .box(4, 4, 3)
    .edges("|Z")        # alle 4 vertikalen Kanten
    .fillet(0.5)
)
save(vertical_fillet, "07b_vertical_edges")

# ─────────────────────────────────────────────────────────────────────────────
# 3) #Z – alle Kanten senkrecht zur Z-Achse (= horizontale Kanten)
#    Ober- und Unterkanten werden gefast.
# ─────────────────────────────────────────────────────────────────────────────
horizontal_chamfer = (
    cq.Workplane("XY")
    .box(4, 4, 3)
    .edges("#Z")        # alle 8 horizontalen Kanten
    .chamfer(0.3)
)
save(horizontal_chamfer, "07c_horizontal_edges")

# ─────────────────────────────────────────────────────────────────────────────
# 4) %CYLINDER – Zylinderflaechen auswählen
#    Ein Zylinder wird in einen Quader eingebettet;
#    nur die gebogene Zylinderflaeche wird mit einem Offset versehen
#    (Shell auf genau dieser Flaeche).
# ─────────────────────────────────────────────────────────────────────────────
cyl_face = (
    cq.Workplane("XY")
    .cylinder(height=4, radius=1.5)
    # Alle zylindrischen Flaechen (= Mantelflaeche)
    .faces("%Cylinder")
    .edges()
    .fillet(0.2)
)
save(cyl_face, "07d_cylinder_face")

# ─────────────────────────────────────────────────────────────────────────────
# 5) Logische Kombinatoren: ">Z and |Z" vs. "<Z or #Z"
#    Hier werden gezielt nur die Oberkanten der vertikalen Seiten gefast.
# ─────────────────────────────────────────────────────────────────────────────
combined = (
    cq.Workplane("XY")
    .box(4, 3, 5)
    # Nur die Kanten, die sowohl am oberen Ende liegen ALS AUCH parallel zu X sind
    .edges(">Z and |X")
    .fillet(0.5)
)
save(combined, "07e_combined_selector")

# ─────────────────────────────────────────────────────────────────────────────
# 6) Numerischer Index-Selektor
#    Bei mehreren Treffern gibt [0], [1], [-1] den n-ten Treffer zurueck.
#    Beispiel: Nur die erste von vier Bohrungsflaechen wird ausgewaehlt.
# ─────────────────────────────────────────────────────────────────────────────
plate = (
    cq.Workplane("XY")
    .box(8, 8, 1)
    .faces(">Z").workplane()
    .rect(5, 5, forConstruction=True)
    .vertices()
    .hole(diameter=1.0)
    # Nur die erste (Index 0) der horizontalen Kanten abrunden – zur Demonstration
    .edges(">Z")
    .item(0)
    .fillet(0.15)
)
save(plate, "07f_index_selector")

print("07_selectors: OK")
