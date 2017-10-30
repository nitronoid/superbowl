#!/usr/bin/python

import prman
import sys
import os


def main():

    filename = 'scene'

    # Instance of Renderman Interface
    ri = prman.Ri()

    # Make sure the output RIB file is indented for clarity
    ri.Option("rib", {"string asciistyle": "indented"})

    # Begin the RIB file
    ri.Begin(filename+'.rib')

    # Include search directories
    ri.Option('searchpath', {'archive': './models', 'shader': './shaders', 'texture': './textures'})
    # Set the display method, I use it to save only when necessary and avoid multiple windows
    ri.Display(filename, 'it', 'rgba')
    # Use perspective projection and set the field of view
    ri.Projection(ri.PERSPECTIVE, {'fov': [50]})
    # Output resolution
    ri.Format(640, 480, 1)

    # Think of these as camera/render settings
    ri.Hider('raytrace', {'int maxsamples': [512]})
    ri.Integrator('PxrPathTracer', 'pt', {'int maxPathLength': [2]})
    # Lower this for faster renders, comment the line for best quality
    ri.PixelVariance([0.2])
    # Camera position
    ri.Translate(0, 0, 10)

    # Start of the scene
    ri.WorldBegin()

    # Create and position our environment dome light
    ri.AttributeBegin()
    ri.Rotate(80, 0, 0, 1)
    ri.Light('PxrDomeLight', 'domeLight', {'string lightColorMap': ['room_hdri.tx']})
    ri.AttributeEnd()

    # The owl
    ri.AttributeBegin()
    # Instantiate some patterns from compiled shaders
    ri.Pattern('oak', 'oakShader')
    ri.Pattern('woodOwl', 'owl')
    # Apply displacement to the owl within 0.2 radius, lower this for faster renders
    ri.Attribute('displacementbound', {'float sphere': [0.2]})
    # Use the displace node with our pattern variables plugged in
    ri.Displace('PxrDisplace', 'displace', {'float dispAmount': [-0.1], 'reference float dispScalar': ['owl:resultF']})
    # Use the PxrDisney for main qualities such as diffuse and spec
    ri.Bxdf('PxrDisney', 'testShad', {'reference color baseColor': ['oakShader:Color']})
    # Read in the model
    ri.ReadArchive('owl.rib')
    ri.AttributeEnd()

    # Draw a floor plane
    ri.AttributeBegin()
    ri.Bxdf('PxrDisney', 'testShad', {'color baseColor': [0.0, 0.7, 0.6]})
    ri.Patch('bilinear', {'P': [10, -3.15, 10, 10, -3.15, -10, -10, -3.15, 10, -10, -3.15, -10]})
    ri.AttributeEnd()

    # End of scene and RIB file
    ri.WorldEnd()
    ri.End()

    return os.EX_OK

if __name__ == "__main__":
    sys.exit(main())
