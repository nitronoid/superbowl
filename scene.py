#!/usr/bin/python

import prman
import sys
import os


''' 
Functions have been used to group together sections of the rib file.
This was done mostly to make the layout clearer, rather than for reusing code.
The most commonly changed settings have been added as params to the functions.
'''


def output_options(ri, filename, res):

    # Include search directories
    ri.Option('searchpath', {'archive': './models', 'shader': './shaders', 'texture': './textures'})
    # Set the display method, I use it to save only when necessary and avoid multiple windows
    ri.Display(filename, 'it', 'rgba')
    # Output resolution
    ri.Format(res[0], res[1], res[2])


def camera_settings(ri, fov, maxsamples, pathlen, pixelvariance, pos):

    # Use perspective projection and set the field of view
    ri.Projection(ri.PERSPECTIVE, {'fov': [fov]})
    ri.Hider('raytrace', {'int maxsamples': [maxsamples]})
    ri.Integrator('PxrPathTracer', 'pt', {'int maxPathLength': [pathlen]})
    # Lower this for faster renders, comment the line for best quality
    ri.PixelVariance([pixelvariance])
    # Camera position
    ri.Translate(pos[0], pos[1], pos[2])


def lighting(ri, env_strength, tri_strength):

    # Basic 3 point lighting
    ri.AttributeBegin()
    ri.Rotate(-35, 0, 1, 0)
    ri.Light('PxrDistantLight', 'keyLight', {'intensity': [0.8 * tri_strength],
                                             'float exposure': [-1],
                                             'float angleExtent': [100]
                                             })
    ri.Rotate(180, 0, 1, 0)
    ri.Light('PxrDistantLight', 'rimLight', {'intensity': [0.4 * tri_strength],
                                             'float exposure': [-1],
                                             'float angleExtent': [100]
                                             })
    ri.Rotate(-95, 0, 1, 0)
    ri.Light('PxrDistantLight', 'fillLight', {'intensity': [0.05 * tri_strength],
                                              'float exposure': [-1],
                                              'float angleExtent': [100]
                                              })
    ri.AttributeEnd()
    # Create and position our environment dome light
    ri.AttributeBegin()
    ri.Rotate(80, 0, 0, 1)
    ri.Light('PxrDomeLight', 'domeLight', {'intensity': [env_strength], 'string lightColorMap': ['room_hdri.tx']})
    ri.AttributeEnd()


def geometry(ri):

    # The owl
    ri.AttributeBegin()
    ri.Rotate(155, 0, 1, 0)
    # Instantiate some patterns from compiled shaders
    ri.Pattern('oak', 'oakShader')
    ri.Pattern('oiledWood', 'woodShader')
    ri.Pattern('woodOwl', 'owl', {'float scale': [1.65], 
                                  'point translate': [-0.15, -0.1, 0],
                                  'float warp': [1],
                                  'float expo': [3],
                                  'float thickness': [0.03],
                                  'float gap': [0.2],
                                  'float fuzz': [0.02]
                                  })
    # Apply displacement to the owl within 0.2 radius, lower this for faster renders
    ri.Attribute('displacementbound', {'float sphere': [0.2]})
    # Use the displace node with our pattern variables plugged in
    ri.Displace('PxrDisplace', 'displace', {'float dispAmount': [-0.1], 'reference float dispScalar': ['owl:resultF']})
    # Use the PxrDisney for main qualities such as diffuse and spec
    ri.Bxdf('PxrDisney', 'testShad', {'reference color baseColor': ['woodShader:resultRGB']})
    # Read in the model
    ri.ReadArchive('owl.rib')
    ri.AttributeEnd()

    # Draw a floor plane
    ri.AttributeBegin()
    ri.Bxdf('PxrDisney', 'testShad', {'color baseColor': [0.0, 0.7, 0.6]})
    ri.Patch('bilinear', {'P': [10, -3.15, 10, 10, -3.15, -10, -10, -3.15, 10, -10, -3.15, -10]})
    ri.AttributeEnd()


def main():

    filename = 'scene'

    # Instance of Renderman Interface
    ri = prman.Ri()

    # Make sure the output RIB file is indented for clarity
    ri.Option("rib", {"string asciistyle": "indented"})

    # Begin the RIB file
    ri.Begin(filename+'.rib')

    # Set up image writing
    output_options(ri, filename=filename, res=(640, 480, 1))
    # Camera settings
    camera_settings(ri, fov=30, maxsamples=512, pathlen=2, pixelvariance=0.2, pos=(0, 0, 17))

    # Start of the scene
    ri.WorldBegin()

    # Scene lighting
    lighting(ri, 0.5, 1)
    # All scene geometry
    geometry(ri)

    # End of scene and RIB file
    ri.WorldEnd()
    ri.End()

    return os.EX_OK


if __name__ == "__main__":

    sys.exit(main())
