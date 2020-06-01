#!/usr/bin/env python

from gimpfu import *


sysParas = {
    "mode":{
        "normal" : 0, #NORMAL-MODE
        "grainMerge" : 21 # GRAIN-MERGE-MODE = 21
    },
    "type":{
        "RGBA":1 # RGBA-IMAGE
    },
    "fill":{
        "fg":0 # FOREGROUND-FILL = 0
    },
    "merge":{
        "bottom":2 # CLIP-TO-BOTTOM-LAYER = 2
    }
}

delt = {
    "Opacity":100
}

paraS = {
    "R" : "R",
    "G" : "G",
    "B" : "B",
    "mask" : "mask",
    "comebined" : "comebined"
}

rgbList = [paraS["R"], paraS["G"], paraS["B"]]


def colorizeRGBA(img, layer, colorR, colorG, colorB):
    # start
    startUpErrorLog()
    gimp.progress_init("spliting...")
    pdb.gimp_image_undo_group_start(img)
    pdb.gimp_message("Hello, world!")


    splitRGBA(img, layer)

    makeMergeLayer(img, layer, 0, colorR)
    makeMergeLayer(img, layer, 2, colorG)
    makeMergeLayer(img, layer, 4, colorB)

    
    hideAlllayers(img)
    mergeRGBLayer(img)
    mixRGBLayer(img, layer)
    ExportSourceMaskTo(img)
    
    # ready to end
    pdb.gimp_selection_none(img)
    pdb.gimp_image_undo_group_end(img)
    pdb.gimp_displays_flush()
    pdb.gimp_progress_end()



def hideAlllayers(img):
    for ly in img.layers:
        ly.visible = False



def startUpErrorLog():
    pdb.gimp_message_set_handler(2)


def findLayerNameIdx(img, layerName):
    for ly in img.layers:
        if ly.name == layerName:
            return img.layers.index(ly)
        else:
            thisLineNoUse = True
    return 0

def getBottomLayer(img):
    return img.layers[len(img.layers)-1]


def ExportSourceMaskTo(img):
    try:
        if getBottomLayer(img).mask is not None:
            pdb.gimp_image_select_item(img, CHANNEL_OP_REPLACE, getBottomLayer(img).mask)
            newMask = pdb.gimp_layer_create_mask(img.layers[0], ADD_SELECTION_MASK)
            img.layers[0].add_mask(newMask)
        else:
            thisLineNoUse = True
    except Exception as err:
        thisLineNoUse = True

    


def mergeRGBLayer(img):
    for ly in rgbList:
        img.layers[findLayerNameIdx(img, ly)-1].visible = True
        img.layers[findLayerNameIdx(img, ly)].visible = True
        mergedLy = pdb.gimp_image_merge_visible_layers(img, sysParas["merge"]["bottom"])
        mergedLy.visible = False



def mixRGBLayer(img, layer):
    mixedlyer = createNewLayer(img, paraS["comebined"], layer)
    xBlocks, yBlocks = countBlocks(layer)
    for yB in range(yBlocks):
            for xB in range(xBlocks):
                tile = tileFor(mixedlyer, xB, yB)
                tileR = tileFor(img.layers[findLayerNameIdx(img, paraS["R"])], xB, yB)
                tileG = tileFor(img.layers[findLayerNameIdx(img, paraS["G"])], xB, yB)
                tileB = tileFor(img.layers[findLayerNameIdx(img, paraS["B"])], xB, yB)
                
                for y in range(tile.eheight):
                    for x in range(tile.ewidth):
                        tile[x,y] = mixPixel(tile[x,y], tileR[x,y])
                        tile[x,y] = mixPixel(tile[x,y], tileG[x,y])
                        tile[x,y] = mixPixel(tile[x,y], tileB[x,y])
    updateLayer(img, mixedlyer)
                        






def tileFor(layer, xB, yB):
    return layer.get_tile(False, yB, xB)


def updateLayer(img, layer):
    layer.flush()
    layer.merge_shadow(True)
    layer.update(0, 0, img.width, img.height)


def createNewLayer(img, name, refLayer):
    result = gimp.Layer(img, name, refLayer.width, refLayer.height, sysParas["type"]["RGBA"], delt["Opacity"], sysParas["mode"]["normal"])
    img.add_layer(result, 0)
    pdb.gimp_edit_clear(result)
    result.flush()
    return result



def countBlocks(layer):
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
    return xBlocks, yBlocks


def splitRGBA(img, layer):   
    # Create the new layers.
    layerR = gimp.Layer(img, paraS["R"], layer.width, layer.height, sysParas["type"]["RGBA"], delt["Opacity"], sysParas["mode"]["normal"])
    layerG = gimp.Layer(img, paraS["G"], layer.width, layer.height, sysParas["type"]["RGBA"], delt["Opacity"], sysParas["mode"]["normal"])
    layerB = gimp.Layer(img, paraS["B"], layer.width, layer.height, sysParas["type"]["RGBA"], delt["Opacity"], sysParas["mode"]["normal"])
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





# for test
def createColor(r,g,b):
    try:
        return gimpcolor.RGB(r/255.0, g/255.0, b/255.0, 1.0)
    except Exception as err:
        return gimpcolor.RGB(0.0, 0.0, 0.0, 1.0)



def makeMergeLayer(img, layer, order, color):
    pdb.gimp_context_set_foreground(color)
    
    ly = gimp.Layer(img, "mergeLayer", layer.width, layer.height, sysParas["type"]["RGBA"], delt["Opacity"], sysParas["mode"]["grainMerge"])
    
    img.add_layer(ly, order)
    
    pdb.gimp_drawable_fill(ly, sysParas["fill"]["fg"])



def mixColorByte(iStr, mStr):
    try:
        i = ord(iStr)
        m = ord(mStr)
        return chr(int(round((i+m) / 2.0)))
    except Exception as err:
        return chr(0)


def mixPixel(iPx, mPx):
    try:
        if iPx[3] == "\x00":
            return mPx
        elif mPx[3] == "\x00":
            return iPx
        else:
            return mixColorByte(iPx[0], mPx[0]) + mixColorByte(iPx[1], mPx[1]) + mixColorByte(iPx[2], mPx[2]) + mixColorByte(iPx[3], mPx[3])
    except Exception as err:
        return "\x00\x00\x00\x00"


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