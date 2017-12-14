# superbowl

## Build
Rendering the scene is as easy as typing  "python scene.py"
Optionally you can rotate the model from the commandline (x-axis only) by using the "-rx" flag.
Optionally you can rotate the environment map from the commandline (x-axis only) by using the "-ex" flag.


## Scripts
There are two scripts included in the repo.
- ribConverter will convert a mesh from maya into a subdivision mesh for Renderman.
- turntable will use the main scene file to render a 360 degree image sequence and video of the scene (it's a bit hacky so you should run the script from the root project directory).


## Textures
The .tx files have not been tracked as they are too large. To compile without errors
you must build them with this mapping:
- Hackberry_pxr128_bmp.tif -> Hackberry_pxr128_bmp.tx
- Hackberry_pxr128.tif     -> Hackberry_pxr128.tx  
- White_Stucco.jpg         -> White_Stucco_bmp.tx
- White_Stucco.jpg         -> White_Stucco.tx 
- woodShop.exr             -> woodShop.tx

All .tx files should be stored in the textures/ directory.
