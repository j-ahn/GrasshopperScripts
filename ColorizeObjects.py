import rhinoscriptsyntax as rs
import Rhino
import scriptcontext
import rhinoscript.utility as rhutil

def ColorizeObjects(aObj):
    rs.EnableRedraw(False) # turn off redraw for faster script exectution.
    
    # the start value of r g b
    r = 1
    g = 0
    b = 0
    
    for i in range(0,len(aObj)): #iterate through all selected objects
        r, g, b = GetColor(r, g, b) #I made a function from your script to modify aColor.
        RGBColor = [int(r * 255), int(g * 255), int(b * 255)]
        rs.ObjectColor(aObj[i], RGBColor)
        
    rs.EnableRedraw(True) #turn screen redraw back on

def GetColor(r, g, b):
    #Color = &HFF000000 Or RGB( r*255, g*255, b * 255 )    
    r = r + 0.6
    if r > 1:
        r = r - 1
        g = g + 0.6
        if g > 1:
            g = g - 1
            b = b + 0.6
            if b > 1 :
                b = b - 1
    
    return r, g, b
    
aObj=rs.GetObjects()
ColorizeObjects(aObj)