import rhinoscriptsyntax as rs
import Rhino
import scriptcontext
import rhinoscript.utility as rhutil

def AddVertices(me, i, vtx1=0, vtx2=0):
    """Add
    face to a mesh"""
    mesh=rhutil.coercemesh(me)

    #select the vertices
    go=Rhino.Input.Custom.GetObject()
    go.GeometryFilter=Rhino.DocObjects.ObjectType.MeshVertex
    go.SetCommandPrompt("Get mesh vertex")
    if vtx1 == 0 or vtx2 == 0:
        go.GetMultiple(3,3)
    else:
        go.GetMultiple(2,2)
    objrefs = go.Objects()
    topology_indices=[item.GeometryComponentIndex.Index for item in objrefs]
    go.Dispose()

    point = []
    for index in topology_indices:
        # in many cases there are multiple vertices in the mesh
        # for a single topology vertex. Just pick the first one
        # in this sample, you will probably have to make a better
        # decision that this for your specific case
        vertex_indices = mesh.TopologyVertices.MeshVertexIndices(index)
        point.append(vertex_indices[0])
    
    if vtx1 != 0 and vtx2 != 0:
        point.append(vtx2)
        point.append(vtx1)
        
    if len(point)==4:
        mesh.Faces.AddFace(point[0], point[1], point[2], point[3])
    else:
        mesh.Faces.AddFace(point[0], point[1], point[2])
    #replace mesh delete point
    scriptcontext.doc.Objects.Replace(me,mesh)
    mesh.Dispose()
    scriptcontext.doc.Views.Redraw()
    if i == 0:
        x,y = point[2],point[3]
    else:
        x,y = point[0],point[1]
        
    return x,y

if( __name__ == "__main__" ):
    me=rs.GetObject("Select a mesh to add face")
    vtx1 = 0
    vtx2 = 0
    for i in range(10):
        print(i)
        AddVertices(me, vtx1,vtx2)
        
        #vtx1, vtx2 = AddVertices(me, i, vtx1,vtx2)