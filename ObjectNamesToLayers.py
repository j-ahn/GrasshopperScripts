import rhinoscriptsyntax as rs

def ObjectNamesToLayers():
    objs = rs.GetObjects("Select objects to transfer to layers",preselect=True)
    if not objs: return
    
    rs.EnableRedraw(False)
    for  obj in objs:
        obj_name = rs.ObjectName(obj)
        if obj_name:
            if not rs.IsLayer(obj_name): rs.AddLayer(obj_name)                
            rs.ObjectLayer(obj,obj_name)        
ObjectNamesToLayers()