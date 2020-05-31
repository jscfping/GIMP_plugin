#!/usr/bin/env python

from gimpfu import *

defaultType = 1 #RGBA-IMAGE
defaultOpacity = 100
defaultMode = 0 #NORMAL-MODE





def colorizeRGBA(img, layer, colorR, colorG, colorB):
    # start
    pdb.gimp_message_set_handler(2)
    gimp.progress_init("spliting...")
    pdb.gimp_image_undo_group_start(img)
    # pdb.gimp_message("Hello, world!")
    pdb.gimp_context_set_foreground(colorR)

    
    
    splitRGBA(img, layer)
    
    # ready to end
    pdb.gimp_image_undo_group_end(img)
    pdb.gimp_displays_flush()
    pdb.gimp_progress_end()




def splitRGBA(img, layer):
    # start
    layer.visible = False

    copyMask(img, layer)
    
    # Create the new layers.
    layerR = gimp.Layer(img, "R", layer.width, layer.height, defaultType, defaultOpacity, defaultMode)
    layerG = gimp.Layer(img, "G", layer.width, layer.height, defaultType, defaultOpacity, defaultMode)
    layerB = gimp.Layer(img, "B", layer.width, layer.height, defaultType, defaultOpacity, defaultMode)
    img.add_layer(layerR, 0)
    img.add_layer(layerG, 1)
    img.add_layer(layerB, 2)
    
    # Clear the new layers.
    pdb.gimp_edit_clear(layerR)
    layerR.flush()
    pdb.gimp_edit_clear(layerG)
    layerG.flush()
    pdb.gimp_edit_clear(layerB)
    layerB.flush()
    
    
    
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
    
                tile = layer.get_tile(False, yB, xB)
                tileR = layerR.get_tile(False, yB, xB)
                tileG = layerG.get_tile(False, yB, xB)
                tileB = layerB.get_tile(False, yB, xB)
                
                for y in range(tile.eheight):
                    for x in range(tile.ewidth):
                        pixel = tile[x,y]
                        
                        if pixel[0] != "\x00":
                            pixelR = pixel[0] + pixel[0] + pixel[0] + "\xff"
                        else:
                            pixelR = "\x00\x00\x00\x00"
                            
                        if pixel[1] != "\x00":
                            pixelG = pixel[1] + pixel[1] + pixel[1] + "\xff"
                        else:
                            pixelG = "\x00\x00\x00\x00"
                            
                        if pixel[2] != "\x00":
                            pixelB = pixel[2] + pixel[2] + pixel[2] + "\xff"
                        else:
                            pixelB = "\x00\x00\x00\x00"
                        
                        tileR[x,y] = pixelR
                        tileG[x,y] = pixelG
                        tileB[x,y] = pixelB


    

    # update
    layerR.flush()
    layerR.merge_shadow(True)
    layerR.update(0, 0, img.width, img.height)

    layerG.flush()
    layerG.merge_shadow(True)
    layerG.update(0, 0, img.width, img.height)

    layerB.flush()
    layerB.merge_shadow(True)
    layerB.update(0, 0, img.width, img.height )




def copyMask(img, layer):

    # Create the new layers.
    layerM = gimp.Layer(img, "MASK", layer.width, layer.height, defaultType, defaultOpacity, defaultMode)
    layerM.visible = False
    img.add_layer(layerM, 0)

    
    # Clear the new layers.
    pdb.gimp_edit_clear(layerM)
    layerM.flush()

    if layer.mask is None:
        return
    else:
        nouse = 0

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



register(
    "python-fu-colorizeRGBA",
    "colorizeRGBA",
    "colorize RGBA layer",
    "jscfping", "jscfping", "2020",
    "_colorizeRGBA",
    "RGB, RGB*",
    [
        (PF_IMAGE, "image", "takes current image", None),
        (PF_DRAWABLE, "drawable", "Input layer", None),
        (PF_COLOUR, "colorR", "R layer color:",(255.0, 255.0, 255.0)),
        (PF_COLOUR, "colorG", "G layer color:",(255.0, 255.0, 255.0)),
        (PF_COLOUR, "colorB", "B layer color:",(255.0, 255.0, 255.0))
    ],
    [],
    colorizeRGBA, menu="<Image>/")

main()