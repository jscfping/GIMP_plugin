#!/usr/bin/env python

from gimpfu import *

def copyMask(img, layer):
    # start
    gimp.progress_init("spliting...")
    pdb.gimp_image_undo_group_start(img)
    
    # Create the new layers.
    layerM = gimp.Layer(img, "MASK", layer.width, layer.height, layer.type, layer.opacity, layer.mode)
    img.add_layer(layerM, 0)

    
    # Clear the new layers.
    pdb.gimp_edit_clear(layerM)
    layerM.flush()

    
    
    
    # for GIMP 64*64 pixels is a block unit for greater 64 pixels
    xBlocks = int(layer.width / 64)
    if(layer.width % 64 > 0):
        xBlocks += 1
    else:
        xBlocks = xBlocks

    yBlocks = int(layer.height / 64)
    if(layer.width % 64 > 0):
        yBlocks += 1
    else:
        yBlocks = yBlocks
    
    
    
    
    for yB in range(yBlocks):
            for xB in range(xBlocks):
    
                tile = layer.mask.get_tile(False, yB, xB)
                tileM = layerM.get_tile(False, yB, xB)
                
                for y in range(tile.eheight):
                    for x in range(tile.ewidth):
                        pixel = tile[x,y]
                        
                        tileM[x,y] = pixel[0] + pixel[0] + pixel[0] + "\xff"
                        


    # update
    layerM.flush()
    layerM.merge_shadow(True)
    layerM.update(0, 0, img.width, img.height)


    
    # ready to end
    pdb.gimp_image_undo_group_end(img)
    pdb.gimp_displays_flush()
    pdb.gimp_progress_end()



register(
    "python-fu-copyMask",
    "copyMask",
    "copy the layer's mask",
    "jscfping", "jscfping", "2020",
    "<Image>/copyMask",
    "RGB, RGB*",
    [],
    [],
    copyMask)

main()