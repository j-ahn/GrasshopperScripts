"""Script by Mitch Heynick 8 October 2013
Trims a set of curves inside or outside multiple closed boundaries
Boundaries may be nested to create regions (trimming between boundaries)
If boundaries overlap, might work anyway, but no guarantees (warning)
All curves may be in 3D, trimming is done with active CPlane projection"""

import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino

def MultiTestInOrOut(testCrv, vols):
    #tests midpoint of curve for containment inside one of several volumes
    #returns True if point is inside at least one of the volumes, otherwise False
    rc=False
    dom=rs.CurveDomain(testCrv)
    if dom==None:
        #debug print "bad domain"
        return
    cmPt=rs.EvaluateCurve(testCrv,(dom[0]+dom[1])/2)
    if cmPt==None:
        #debug print "bad curve"
        return
    for vol in vols:
        if rs.IsPointInSurface(vol,cmPt,True,sc.doc.ModelAbsoluteTolerance):
            #curve is inside one of the volumes
            rc=True
            break
    return rc
    
def CheckPlanarCurvesForCollision(crvs):
    #curves must be planar, returns True if any two curves overlap
    for i in range(len(crvs)-1):
        for j in range(i+1,len(crvs)):
            if rs.PlanarCurveCollision(crvs[i],crvs[j]): return True
    return False

def MultiNestedBoundaryTrimCurves():
    msg="Select closed boundary curves for trimming"
    TCrvs = rs.GetObjects(msg, 4, preselect=False)
    if not TCrvs: return
    
    cCrvs=[crv for crv in TCrvs if rs.IsCurveClosed(crv)]
    if len(cCrvs)==0:
        print "No closed trim curves found"
        return
    rs.LockObjects(cCrvs)
    
    origCrvs = rs.GetObjects("Select curves to trim", 4)
    rs.UnlockObjects(cCrvs)
    if not origCrvs : return
    
    #plane which is active when trim curve is chosen
    refPlane = rs.ViewCPlane()
    
    if sc.sticky.has_key("TrimSideChoice"):
        oldTSChoice = sc.sticky["TrimSideChoice"]
    else:
        oldTSChoice=True
    
    choice = [["Trim", "Outside", "Inside"]]
    res = rs.GetBoolean("Side to trim away?", choice, [oldTSChoice])
    if not res: return
    trimIns = res[0] #False=Outside
    
    tol=sc.doc.ModelAbsoluteTolerance
    bb=rs.BoundingBox(origCrvs,refPlane) #CPlane box, world coords
    if not bb: return
    zVec=refPlane.ZAxis
    
    rs.EnableRedraw(False)
    botPlane=Rhino.Geometry.Plane(bb[0]-zVec,zVec) #check
    xform=rs.XformPlanarProjection(botPlane)
    cutCrvs=rs.TransformObjects(cCrvs,xform,True)
    ccc=CheckPlanarCurvesForCollision(cutCrvs)
    if ccc:
        msg="Boundary curves overlap, results may be unpredictable, continue?"
        res=rs.MessageBox(msg,1+32)
        if res!= 1: return
    bSrfs=rs.AddPlanarSrf(cutCrvs)
    rs.DeleteObjects(cutCrvs)
    if bSrfs == None: return
    
    line=rs.AddLine(bb[0]-zVec,bb[4]+zVec)
    vols=[]
    for srf in bSrfs:
        ext=rs.ExtrudeSurface(srf,line,True)
        if ext != None: vols.append(ext)
    rs.DeleteObjects(bSrfs)
    rs.DeleteObject(line)
    if len(vols)==0: return
    exGroup=rs.AddGroup()
    rs.AddObjectsToGroup(vols,exGroup)
    
    rs.Prompt("Splitting curves...")
    rs.SelectObjects(origCrvs)
    rs.Command("_Split _-SelGroup " + exGroup + " _Enter", False)
    splitRes=rs.LastCreatedObjects()
    rs.DeleteGroup(exGroup)
    
    rs.Prompt("Classifying trims...")
    noSplit=[]
    for crv in origCrvs:
        #add curve to list if it has not been split (still exists in doc)
        id=sc.doc.Objects.Find(crv)        
        if id != None: noSplit.append(crv)
        
    errors=0
    if splitRes:
        if len(noSplit)>0: splitRes.extend(noSplit)
        for crv in splitRes:
            inside=MultiTestInOrOut(crv,vols)
            if inside != None:
                if (inside and trimIns) or (not inside and not trimIns):
                    rs.DeleteObject(crv)
            else:
                errors+=1
    rs.DeleteObjects(vols)
    if errors>0: print "Problems with {} curves".format(errors)
    sc.sticky["TrimSideChoice"] = trimIns

MultiNestedBoundaryTrimCurves()