import cadquery as cq
import random as random
nippleradius = 0.2
l = 10
w = 4
h = 10
sponge = cq.Workplane('XY').box(l, w, h, centered=False)
resX = 5
resY = 2
resZ = 5
spheres = cq.Workplane('XY')
#result = result.union(sphere3)
for x in range(0,resX+1):
    for y in range(0,resY+1):
        for z in range(0,resZ+1):
            translation = (l/resX * x, w/resY * y, h/resZ * z)
            #translation = (l/resX*x, 1,h/resZ * z)
            aSphere = cq.Workplane('XY').sphere(random.random()/2 + 0.1).translate(translation)
            spheres.add(aSphere)
sponge = sponge.cut(spheres)
#result = cq.Workplane().box(1,1,1).faces().edges().fillet(0.1)
cq.exporters.export(sponge, "simpleSponge.step")
#cq.exporters.export(result, "nippledsphere.stl",  tolerance= 0.01, angularTolerance = 0.1)
#cq.exporters.export(sponge, "simpleSponge.stl")
#cq.exporters.export(result.section(),'result.dxf')
