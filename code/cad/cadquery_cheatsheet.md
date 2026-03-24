# CadQuery Cheatsheet

## Grundprinzip

CadQuery arbeitet mit einer **Fluent-API** – Methoden werden per `.` verkettet:

```python
import cadquery as cq

result = (
    cq.Workplane("XY")   # Arbeitsebene wählen
    .box(4, 4, 2)         # Grundkörper erzeugen
    .faces(">Z")          # Fläche selektieren
    .workplane()          # neue Arbeitsebene auf dieser Fläche
    .hole(1.0)            # Operation ausführen
)
```

---

## Geometrie-Hierarchie: Vertices · Edges · Faces

Ein 3D-Körper besteht aus drei Ebenen geometrischer Elemente:

```
Solid (Körper)
 └── Faces   – Flächen, die den Körper begrenzen  (eben, zylindrisch, …)
      └── Edges   – Kanten, die Flächen verbinden  (gerade Linie, Kreis, …)
           └── Vertices – Punkte, an denen Kanten zusammentreffen
```

Mit `.vertices()`, `.edges()` und `.faces()` wechselst du in CadQuery
in den jeweiligen Selektions-Kontext. Anschließende Operationen (fillet, hole, …)
wirken dann genau auf die ausgewählten Elemente.

```python
result = cq.Workplane("XY").box(4, 4, 2)

# Faces – alle Flächen abfragen
result.faces()          # alle 6 Flächen des Quaders selektiert

# Edges – alle Kanten abfragen
result.edges()          # alle 12 Kanten des Quaders selektiert

# Vertices – alle Punkte abfragen
result.vertices()       # alle 8 Eckpunkte des Quaders selektiert
```

Ohne Selektor-Argument werden **alle** Elemente des jeweiligen Typs zurückgegeben.
Mit einem Selektor-Argument wird gefiltert – das sind die Selektoren, die weiter
unten erklärt werden:

```python
result.faces()          # alle 6 Flächen
result.faces(">Z")      # nur die Deckfläche   (Selektor → siehe unten)
result.edges("|Z")      # nur die 4 vertikalen Kanten
result.vertices()       # alle 8 Eckpunkte
```

Typischer Ablauf – Fläche auswählen, Arbeitsebene darauf, dann zeichnen:

```python
(
    cq.Workplane("XY")
    .box(4, 4, 2)
    .faces(">Z")         # Deckfläche als aktive Fläche setzen
    .workplane()         # Arbeitsebene auf diese Fläche legen
    .circle(0.8)         # Kreis auf der neuen Ebene zeichnen
    .extrude(1)          # Kreis nach oben extrudieren → Zylinder entsteht
)
```

---

## Arbeitsebenen (Workplane)

| Ebene | Normale zeigt nach |
|-------|--------------------|
| `"XY"` | Z |
| `"XZ"` | Y |
| `"YZ"` | X |

```python
# Neue Arbeitsebene direkt beim Erzeugen angeben
cq.Workplane("XY")   # Ebene liegt in XY, Normalenvektor zeigt in Z
cq.Workplane("XZ")   # Ebene liegt in XZ, Normalenvektor zeigt in Y
cq.Workplane("YZ")   # Ebene liegt in YZ, Normalenvektor zeigt in X

# Ebene mit Versatz vom Ursprung
cq.Workplane("XY", origin=(0, 0, 5))   # 5 Einheiten über XY

# Ebene um Winkel drehen
cq.Workplane("XY").transformed(rotate=(0, 0, 45))  # 45° um Z-Achse

# Auf einer Fläche eine neue Ebene aufspannen (Selektoren → siehe unten)
# .faces(">Z").workplane()
```

---

## Grundkörper (Primitives)

```python
.box(length, width, height)             # Quader, zentriert
.box(l, w, h, centered=False)           # Quader, Ecke bei Ursprung
.sphere(radius)                         # Kugel
.cylinder(height, radius)              # Zylinder
.cone(height, radius1, radius2)        # Kegelstumpf
```

---

## 2D-Profile → 3D

```python
# Extrusion
.rect(w, h).extrude(depth)
.circle(r).extrude(depth)
.polygon(sides, diameter).extrude(depth)

# Freies Profil zeichnen und extrudieren
.polyline([(0,0),(0,4),(2,4),(2,0)]).close().extrude(5)

# Revolution (um Achse drehen)
.circle(0.5).revolve(360, (0,0,0), (0,1,0))

# Sweeping (Profil entlang Pfad)
.circle(0.3).sweep(path)
```

---

## Selektoren – Übersicht

Selektoren wählen **Faces**, **Edges** oder **Vertices** gezielt aus.

### Richtungsselektoren

| Selektor | Bedeutung |
|----------|-----------|
| `">X"` | Fläche/Kante am weitesten in +X |
| `"<X"` | Fläche/Kante am weitesten in −X |
| `">Y"`, `"<Y"` | analog für Y |
| `">Z"`, `"<Z"` | analog für Z |

```python
.faces(">Z")           # Deckfläche
.faces("<Z")           # Bodenfläche
.faces(">X")           # rechte Seitenfläche
```

### Orientierungsselektoren

| Selektor | Bedeutung |
|----------|-----------|
| `"\|Z"` | parallel zur Z-Achse (vertikale Kanten) |
| `"\|X"` | parallel zur X-Achse |
| `"#Z"` | senkrecht zu Z (horizontale Kanten/Flächen) |
| `"+Z"` | Normalenvektor zeigt in +Z |
| `"-Z"` | Normalenvektor zeigt in −Z |

```python
.edges("|Z")           # alle 4 vertikalen Kanten
.edges("#Z")           # alle horizontalen Kanten
.faces("+Y")           # Fläche, die in +Y zeigt
```

### Geometrietypen (`%`)

```python
.faces("%Plane")       # alle ebenen Flächen
.faces("%Cylinder")    # alle Zylindermantelflächen
.faces("%Sphere")      # alle Kugeloberflächen
.edges("%Circle")      # alle kreisförmigen Kanten (z.B. Bohrungsränder)
.edges("%Line")        # alle geraden Kanten
```

### Logische Kombinatoren

```python
.edges(">Z and |X")    # oben UND parallel zu X
.edges(">Z or <Z")     # oben ODER unten
.edges("not |Z")       # alle außer den vertikalen
```

### Index-Selektor

Wenn mehrere Elemente gefunden werden, kann man per Index auswählen:

```python
.edges(">Z").item(0)   # Erstes Ergebnis
.edges(">Z").item(-1)  # Letztes Ergebnis
```

---

## Boolesche Operationen

```python
a = cq.Workplane("XY").box(3, 3, 3)
b = cq.Workplane("XY").sphere(2)

a.union(b)       # Vereinigung  (a + b)
a.cut(b)         # Differenz    (a − b)
a.intersect(b)   # Schnittmenge (a ∩ b)
```

---

## Fasen & Abrundungen

```python
# Fillet (Rundung)
.edges("|Z").fillet(0.5)          # alle vertikalen Kanten runden
.edges(">Z").fillet(0.3)          # Oberkante runden

# Chamfer (Fase / 45°-Abschnitt)
.edges("|Z").chamfer(0.4)
.edges("#Z").chamfer(0.2)
```

---

## Bohrungen & Muster

```python
# Einfache Durchgangsbohrung
.faces(">Z").workplane().hole(diameter=1.0)

# Bohrung mit Senkung (Counterbore)
.cboreHole(diameter=0.5, cboreDiameter=1.0, cboreDepth=0.3)

# Bohrung mit Kegelsenkung (Countersink)
.cskHole(diameter=0.5, cskDiameter=1.0, cskAngle=82)

# Bohrungen auf Rechteck-Raster verteilen
.rect(4, 4, forConstruction=True).vertices().hole(0.5)

# Bohrungen auf Kreismuster verteilen (6 Stück)
.polarArray(radius=3, startAngle=0, angle=360, count=6).hole(0.4)
```

---

## Shell (Aushöhlen)

```python
# Box mit 0.2 Wandstärke, Deckel offen
.box(4, 4, 5).faces(">Z").shell(-0.2)
```

---

## Transformationen

```python
.translate((x, y, z))                        # Verschieben
.rotate((0,0,0), (0,0,1), 45)               # Drehen: Punkt, Achse, Winkel
.mirror("XY")                                # Spiegeln an Ebene
.scale(factor)                               # Skalieren (uniform)
```

---

## Export

```python
from cadquery import exporters

cq.exporters.export(result, "out.step")   # STEP – universelles CAD-Format
cq.exporters.export(result, "out.stl")    # STL  – für 3D-Druck
cq.exporters.export(result, "out.svg",    # SVG  – 2D-Konstruktionsansicht
    opt={"projectionDir": (1, 1, 0.5), "showAxes": True})
cq.exporters.export(result, "out.dxf")   # DXF  – 2D-Zeichnung (faces(">Z") zuvor)
```

---

## Tutorials in diesem Ordner

| Datei | Thema |
|-------|-------|
| [01_primitives.py](01_primitives.py) | Box, Sphere, Cylinder |
| [02_transforms.py](02_transforms.py) | translate, rotate |
| [03_booleans.py](03_booleans.py) | union, cut, intersect |
| [04_extrude_revolve.py](04_extrude_revolve.py) | extrude, revolve, L-Profil |
| [05_chamfer_fillet_holes.py](05_chamfer_fillet_holes.py) | chamfer, fillet, cboreHole |
| [06_shell_selectors.py](06_shell_selectors.py) | shell, Workplane-Ketten |
| [07_selectors.py](07_selectors.py) | alle Selektoren im Detail |
