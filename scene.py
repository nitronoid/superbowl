#!/usr/bin/python

import prman

ri = prman.Ri()
ri.Option("rib", {"string asciistyle": "indented"})

filename = 'scene'

ri.Begin(filename+'.rib')

ri.Option('searchpath', {'archive' : './models', 'shader' : './shaders', 'texture' : './textures'})

ri.Display(filename, 'it', 'rgba')
ri.Projection(ri.PERSPECTIVE,{'fov' : [50]})
ri.Format(640,480,1)

ri.Hider('raytrace', {'int maxsamples' : [512]})
ri.Integrator('PxrPathTracer', 'spt', {'int maxPathLength' : [2]})
ri.PixelVariance([0.2])

ri.Translate(0,0,10)
ri.WorldBegin()

ri.AttributeBegin()
ri.TransformBegin()
ri.Rotate(80,0,0,1)
ri.Light('PxrDomeLight','domeLight',{'string lightColorMap' : ['room_hdri.tx']})
ri.TransformEnd()
ri.AttributeEnd()

ri.AttributeBegin()
ri.Pattern('oak','oakShader')
ri.Pattern('woodOwl','owl')
ri.Attribute('displacementbound', {'float sphere' : [0.2]})
ri.Displace('PxrDisplace', 'displace', {'float dispAmount' : [-0.1], 'reference float dispScalar' : ['owl:resultF']})
ri.Bxdf('PxrDisney', 'testShad', {'reference color baseColor' : ['oakShader:Color']})
ri.ReadArchive('owl.rib')
ri.AttributeEnd()

ri.AttributeBegin()
ri.Bxdf('PxrDisney', 'testShad', {'color baseColor' : [0.0,0.7,0.6]})
ri.Patch('bilinear',{'P' : [10, -3.15, 10, 10, -3.15, -10, -10, -3.15, 10, -10, -3.15, -10]})
ri.AttributeEnd()

ri.WorldEnd()

ri.End()