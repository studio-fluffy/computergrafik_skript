import cadquery as cq
radius = 0.2
sphere1 = cq.Workplane('XY').sphere(0.91)
sphere2 = cq.Workplane('XY').sphere(radius).translate((1-radius/2,0,0))
sphere3 = cq.Workplane('XY').sphere(radius).translate((1.05 + radius,0,0))
sphere4 = sphere2.cut(sphere3)
result = sphere1

resY = 6
#result = result.union(sphere3)

for v in range(0,resY):

    aSphere = sphere4.rotate((0,0,0), (0,1,0), (v/resY)*360)
    result = result.union(aSphere)

result = result.faces().fillet(0.09)  
cq.exporters.export(result, "./code/spikedsphere.step")
cq.exporters.export(result, "./code/spikedsphere.stl")
