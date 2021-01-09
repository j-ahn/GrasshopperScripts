"""
Created: 4/12/2019
Rotate cross-section lines to 2D (XY - plane)
@author: Jiwoo Ahn
"""


import rhinoscriptsyntax as rs
import math

def Section2D():
    #"Create cross-section and rotate to 2D plane"
    
    # Select objects to draw section from
    objects = rs.GetObjects("Select objects to rotate", rs.filter.curve)
    # Select cross section plane
    sectionplane = rs.GetObject("Select cross-section line", rs.filter.curve)

    # Calculate orientation of cross-section plane
    startpt = rs.CurveStartPoint(sectionplane)
    midpt = rs.CurveMidPoint(sectionplane)
    endpt = rs.CurveEndPoint(sectionplane)
    
    x1, y1 = startpt[0], startpt[1]
    x2, y2 = endpt[0], endpt[1]
    
    rad2deg = 180 / math.pi
    angle = math.atan((y2-y1)/(x2-x1)) * rad2deg
    
    # rotate cross-section objects to 2D plane
    rs.RotateObjects(objects, midpt, -angle)
    rs.RotateObjects(objects, midpt, -90, [1,0,0])
  

if( __name__ == "__main__" ):
    Section2D()