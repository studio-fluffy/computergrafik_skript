import cadquery as cq

# Größe des Quaders
length = 50.0
width = 30.0
height = 20.0

# Anzahl der Löcher und deren Größe
num_holes = 20
hole_diameter = 5.0

# Berechnen Sie die Schrittweite für die gleichmäßige Verteilung der Löcher
step = min(length, width) / (num_holes**0.5)

# Erstelle den Quader
box = cq.Workplane("XY").box(length, width, height)

# Erstelle die Löcher
for i in range(num_holes):
    # Berechnen Sie die Position des Lochs basierend auf der Schrittweite
    x = ((i % int(num_holes**0.5)) - int(num_holes**0.5)/2) * step
    y = ((i // int(num_holes**0.5)) - int(num_holes**0.5)/2) * step
    z = 0
    
    # Erstelle den Zylinder und ziehe ihn aus dem Quader
    hole = cq.Workplane("XY").circle(hole_diameter/2).extrude(height)
    box = box.cut(hole.translate((x, y, z)))

cq.exporters.export(box, "box_with_holes.stl")
cq.exporters.export(box, "box_with_holes.step")

#show_object(box)