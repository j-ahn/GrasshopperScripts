import rhinoscriptsyntax as rs
import Rhino
import scriptcontext
import rhinoscript.utility as rhutil

def AddVertices(me):
    """Add
    face to a mesh"""
    
    mesh=rhutil.coercemesh(me)

    #select the verticessepol
    go=Rhino.Input.Custom.GetObject()
    go.GeometryFilter=Rhino.DocObjects.ObjectType.MeshVertex
    go.SetCommandPrompt("Get mesh vertex")
    go.GetMultiple(3,3)

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
        
    mesh.Faces.AddFace(point[0], point[1], point[2])
    #replace mesh delete point
    scriptcontext.doc.Objects.Replace(me,mesh)
    mesh.Dispose()
    scriptcontext.doc.Views.Redraw()

if( __name__ == "__main__" ):
    me=rs.GetObject("Select a mesh to add face")

    for i in range(10):
        print(i)
        AddVertices(me)