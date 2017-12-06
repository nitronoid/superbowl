#!/usr/bin/python

import prman
import sys
import os
import glob
import argparse
import subprocess
import math


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


def camera_settings(ri, fov, maxsamples, pathlen, pixelvariance, pos, rot):
    # Use perspective projection and set the field of view
    ri.Projection(ri.PERSPECTIVE, {'fov': [fov]})
    ri.Hider('raytrace', {'int maxsamples': [maxsamples]})
    ri.Integrator('PxrPathTracer', 'pt', {'int maxPathLength': [pathlen]})
    # Lower this for faster renders, comment the line for best quality
    ri.PixelVariance([pixelvariance])
    # Camera position
    ri.Translate(pos[0], pos[1], pos[2])
    rotation = math.sqrt(sum([x*x for x in rot]))
    if rotation != 0.0:
        vec = [x / rotation for x in rot]
        ri.Rotate(rotation, vec[0], vec[1], vec[2])
    ri.Exposure(1.0, 2.2)
    ri.DepthOfField(0.15, 0.05, 14.5)


def lighting(ri, env_strength, rx):
    # Create and position our environment dome light
    ri.AttributeBegin()
    ri.Rotate(rx, 0, 1, 0)
    ri.Rotate(-120, 1, 0, 0)
    ri.Light('PxrDomeLight', 'domeLight', {'intensity': [env_strength], 'string lightColorMap': ['woodShop.tx']})
    ri.AttributeEnd()


def owl(ri, rotate_x):
    # The owl
    ri.AttributeBegin()
    ri.ShadingRate(0.5)
    ri.Rotate(rotate_x, 0, 1, 0)
    # Instantiate some patterns from compiled shaders
    ri.Pattern('oiledWood', 'woodShader', {'float eyeScale': [1.65],
                                           'point eyeTranslate': [0.21, 0.3, 0],
                                           'float eyeRotation': [7],
                                           'float eyeWarp': [1],
                                           'float eyeExponent': [3],
                                           'float eyeThickness': [0.04],
                                           'float eyeGap': [0.2],
                                           'float eyeFuzz': [0.02]
                                           })
    # Apply displacement to the owl within 0.2 radius, lower this for faster renders
    ri.Attribute('displacementbound', {'float sphere': [0.2]})
    # Use the displace node with our pattern variables plugged in
    ri.Displace('PxrDisplace', 'displace', {'float dispAmount': [-0.1],
                                            'reference float dispScalar': ['woodShader:disp']
                                            })
    # Use the PxrDisney for main qualities such as diffuse and spec
    ri.Bxdf('PxrDisney', 'testShad', {'reference color baseColor': ['woodShader:resultRGB'],
                                      'float clearcoat': [0.8],
                                      'float clearcoatGloss': [1],
                                      'reference float specular': ['woodShader:spec'],
                                      'reference float roughness': ['woodShader:rough']
                                      })
    # Read in the model
    ri.ReadArchive('owl.rib')
    ri.AttributeEnd()


def environment(ri):
    # Draw a floor plane
    ri.TransformBegin()
    ri.Rotate(7.5, 0, 1, 0)
    ri.Scale(5, 1, 5)
    ri.AttributeBegin()
    ri.Pattern('tile', 'table', {'float tile': [20], 'string name': ['Hackberry_pxr128']})
    ri.Bxdf('PxrDisney', 'testShad', {'reference color baseColor': ['table:resultRGB'],
                                      'float specular': [0.6],
                                      'float roughness': [0.6],
                                      'float clearcoat': [1],
                                      'float clearcoatGloss': [1]
                                      })
    ri.Attribute('displacementbound', {'float sphere': [0.2]})
    # Use the displace node with our pattern variables plugged in
    ri.Displace('PxrDisplace', 'displace', {'float dispAmount': [0.1],
                                            'reference vector dispVector': ['table:resultDisp']
                                            })
    ri.Patch('bilinear', {'P': [10, -3.15, 10, 10, -3.15, -10, -10, -3.15, 10, -10, -3.15, -10]})
    ri.AttributeEnd()
    ri.AttributeBegin()
    ri.Pattern('tile', 'wall', {'float tile': [15], 'string name': ['White_Stucco']})
    ri.Bxdf('PxrDisney', 'testShad', {'reference color baseColor': ['wall:resultRGB'],
                                      'float specular': [0.6],
                                      'float roughness': [0.6],
                                      'float clearcoat': [1],
                                      'float clearcoatGloss': [1]
                                      })
    ri.Translate(0, 0, 3.65)
    ri.Rotate(90, 1, 0, 0)
    ri.Patch('bilinear', {'P': [10, -3.15, 10, 10, -3.15, -10, -10, -3.15, 10, -10, -3.15, -10]})
    ri.AttributeEnd()
    ri.TransformEnd()


def scene(name, rx, ex, save):
    # Instance of Renderman Interface
    ri = prman.Ri()

    # Make sure the output RIB file is indented for clarity
    ri.Option("rib", {"string asciistyle": "indented"})

    # Begin the render
    ri.Begin('__render')

    # Set up image writing
    output_options(ri, filename=name, res=(853, 480, 1), save=save)

    # Camera settings
    camera_settings(ri,
                    fov=30,
                    maxsamples=2048,
                    pathlen=2,
                    pixelvariance=0.01,
                    pos=(0, 0, 16),
                    rot=(-7.5, 0, 0)
                    )

    # Start of the scene
    ri.WorldBegin()

    # Scene lighting
    lighting(ri, env_strength=5, rx=ex)
    # Draw the owl
    owl(ri, rotate_x=rx)
    # Draw the environment geometry
    environment(ri)

    # End of scene and RIB file
    ri.WorldEnd()
    ri.End()

    return os.EX_OK


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-rx', '--rotationx', type=float, default=160,
                        help='The rotation in the x axis applied to the model')
    parser.add_argument('-ex', '--environmentx', type=float, default=0,
                        help='The rotation in the x axis applied to the model')
    args = parser.parse_args()

    for f in glob.iglob('shaders/*.osl'):
        print('Compiling shader: ' + f)
        subprocess.call(["oslc", '-o', f[:-1] + 'o', f])

    scene('scene', args.rotationx, args.environmentx, False)


if __name__ == "__main__":
    sys.exit(main())
