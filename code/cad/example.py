import cadquery as cq
from cadquery import exporters
from pathlib import Path

result = (
	cq.Workplane("XY")
	.box(1, 2, 3)
	.faces(">Z")
	.vertices()
	.hole(0.3)
)

output_path = Path(__file__).with_suffix(".stl")
exporters.export(result, str(output_path))
print(f"STL gespeichert: {output_path}")
