import rhinoscriptsyntax as rs
from scriptcontext import doc

def renameLayers():
    
    LayersList = [layer for layer in doc.Layers if 'Southern Mod' in str(layer.Name)]
    
    for layer in LayersList:
        layerName = layer.Name[13:]
        layer.Name = layerName
        
    return

renameLayers()