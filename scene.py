#!/usr/bin/python

import prman
import sys
import os
import argparse


''' 
Functions have been used to group together sections of the rib file.
This was done mostly to make the layout clearer, rather than for reusing code.
The most commonly changed settings have been added as params to the functions.
'''


def output_options(ri, filename, res, save):
    # Include search directories
    ri.Option('searchpath', {'archive': './models', 'shader': './shaders', 'texture': './textures'})
    # Set the display method, I use it to save only when necessary and avoid multiple windows
    out = 'it'
    if save:
        filename += '.tiff'
        out = 'file'
    ri.Display(filename, out, 'rgba')
    # Output resolution
    ri.Format(res[0], res[1], res[2])
    # Convert from float
    ri.Quantize('rgba', 255, 0, 255, 0)


def camera_settings(ri, fov, maxsamples, pathlen, pixelvariance, pos):
    # Use perspective projection and set the field of view
    ri.Projection(ri.PERSPECTIVE, {'fov': [fov]})
    ri.Hider('raytrace', {'int maxsamples': [maxsamples]})
    ri.Integrator('PxrPathTracer', 'pt', {'int maxPathLength': [pathlen]})
    # Lower this for faster renders, comment the line for best quality
    ri.PixelVariance([pixelvariance])
    # Camera position
    ri.Translate(pos[0], pos[1], pos[2])
    ri.Exposure(1.0, 2.2)


def lighting(ri, env_strength, tri_strength):
    # Basic 3 point lighting
    ri.AttributeBegin()
    ri.Rotate(-35, 0, 1, 0)
    ri.Light('PxrDistantLight', 'keyLight', {'intensity': [0.5 * tri_strength],
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
    ri.Rotate(0, 0, 1, 0)
    ri.Rotate(-120, 1, 0, 0)
    ri.Light('PxrDomeLight', 'domeLight', {'intensity': [env_strength], 'string lightColorMap': ['woodShop.tx']})
    ri.AttributeEnd()


def geometry(ri, rotate_x):
    # The owl
    ri.AttributeBegin()
    ri.Rotate(rotate_x, 0, 1, 0)
    # Instantiate some patterns from compiled shaders
    ri.Pattern('oiledWood', 'woodShader', {'float scale': [1.65],
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
    ri.Displace('PxrDisplace', 'displace', {'float dispAmount': [-0.1], 'reference float dispScalar': ['woodShader:disp']})
    # Use the PxrDisney for main qualities such as diffuse and spec
    ri.Bxdf('PxrDisney', 'testShad', {'reference color baseColor': ['woodShader:resultRGB'], 
                                      'float clearcoat' : [1],
                                      'float clearcoatGloss' : [1],
                                      'reference float specular' : ['woodShader:spec'],
                                      'reference float roughness' : ['woodShader:rough']
                                      })
    # Read in the model
    ri.ReadArchive('owl.rib')
    ri.AttributeEnd()

    # Draw a floor plane
    ri.AttributeBegin()
    ri.Bxdf('PxrDisney', 'testShad', {'color baseColor': [0.0, 0.7, 0.6]})
    ri.Patch('bilinear', {'P': [10, -3.15, 10, 10, -3.15, -10, -10, -3.15, 10, -10, -3.15, -10]})
    ri.AttributeEnd()


def main(name, rx, save):
    # Instance of Renderman Interface
    ri = prman.Ri()

    # Make sure the output RIB file is indented for clarity
    ri.Option("rib", {"string asciistyle": "indented"})

    # Begin the render
    ri.Begin('__render')

    # Set up image writing
    output_options(ri, filename=name, res=(640, 480, 1), save=save)

    # Camera settings
    camera_settings(ri, fov=30, maxsamples=1024, pathlen=2, pixelvariance=0.2, pos=(0, 0, 17))

    # Start of the scene
    ri.WorldBegin()

    # Scene lighting
    lighting(ri, env_strength=1.5, tri_strength=1)
    # All scene geometry
    geometry(ri, rotate_x=rx)

    # End of scene and RIB file
    ri.WorldEnd()
    ri.End()

    return os.EX_OK


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-rx', '--rotationx', type=float, default=160,
                        help='The rotation in the x axis applied to the model')
    args = parser.parse_args()

    sys.exit(main('scene', args.rotationx, False))
