import FreeCAD, FreeCADGui, Draft, Part
from pivy import coin

class ImagePlane:
    def __init__(self, obj, image2):
        self.image=image2
        obj.addProperty("App::PropertyFloat","xScale","ImagePlane","X scale of the image plane").xScale=1.0
        obj.addProperty("App::PropertyFloat","yScale","ImagePlane","Y scale of the image plane").yScale=1.0
        obj.Proxy = self
   
    def onChanged(self, fp, prop):
        if prop=="xScale" or prop=="yScale":
            sx=fp.xScale
            sy=fp.yScale
            width = sx*self.image.width
            height = sy*self.image.height
        #FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
 
    def execute(self, fp):
        sx=fp.xScale
        sy=fp.yScale
        width = sx*self.image.width
        height = sy*self.image.height
        v1 = FreeCAD.Vector(-width/2,-height/2,0)
        v2 = FreeCAD.Vector(width/2,-height/2,0)
        v3 = FreeCAD.Vector(width/2,height/2,0)
        v4 = FreeCAD.Vector(-width/2,height/2,0)
        wire = Part.makePolygon([v1,v2,v3,v4,v1])
        face = Part.Face(wire)
        fp.Shape = face

    def __getstate__(self):
        return None
 
    def __setstate__(self,state):
        return None
        
 
class ViewProviderImagePlane:
    def __init__(self, obj, image2):
        obj.ShapeColor=(1.0,1.0,1.0)
        self.image=image2
        self.width=self.image.width
        self.height=self.image.height
        obj.Proxy = self
 
    def attach(self, obj):
        self.shaded = coin.SoGroup()
        self.wireframe = coin.SoGroup()
        self.scale = coin.SoScale()
        self.material=coin.SoMaterial()
        self.color = coin.SoBaseColor()
        self.material.transparency.setValue(obj.Transparency/100)
        self.material.emissiveColor.setValue(coin.SbColor(1,1,1))
        obj.Selectable=False
        
        ipVertexes = coin.SoVertexProperty()

        # Define the square's spatial coordinates
        ipVertexes.vertex.set1Value(0, coin.SbVec3f(-self.width/2, -self.height/2, 0))
        ipVertexes.vertex.set1Value(1, coin.SbVec3f( self.width/2, -self.height/2, 0))
        ipVertexes.vertex.set1Value(2, coin.SbVec3f( self.width/2,  self.height/2, 0))
        ipVertexes.vertex.set1Value(3, coin.SbVec3f(-self.width/2,  self.height/2, 0))

        # Define the square's normal
        ipVertexes.normal.set1Value(0, coin.SbVec3f(0, 0, 1))

        # Define the square's texture coordinates
        ipVertexes.texCoord.set1Value(0, coin.SbVec2f(0, 1))
        ipVertexes.texCoord.set1Value(1, coin.SbVec2f(1, 1))
        ipVertexes.texCoord.set1Value(2, coin.SbVec2f(1, 0))
        ipVertexes.texCoord.set1Value(3, coin.SbVec2f(0, 0))

        # Define a FaceSet
        ipFaceSet = coin.SoFaceSet()
        ipFaceSet.numVertices.set1Value(0, 4)
        ipFaceSet.vertexProperty.setValue(ipVertexes)

        self.shaded.addChild(self.scale)
        self.shaded.addChild(self.material)
        self.shaded.addChild(self.color)
        self.shaded.addChild(ipFaceSet)
        obj.addDisplayMode(self.shaded,"Shaded");
        style=coin.SoDrawStyle()
        style.style = coin.SoDrawStyle.LINES
        self.wireframe.addChild(style)
        self.wireframe.addChild(self.scale)
        self.wireframe.addChild(self.material)
        self.wireframe.addChild(self.color)
        self.wireframe.addChild(ipFaceSet)
        obj.addDisplayMode(self.wireframe,"Wireframe");
        self.onChanged(obj,"Transparency")
        if self.image is not None:
            rootnode = obj.RootNode
            tex=self.image.getTexture()
            rootnode.insertChild(tex,1)
 
    def updateData(self, fp, prop):
        sx=fp.getPropertyByName("xScale")
        sy=fp.getPropertyByName("yScale")
        self.width = sx*self.image.width
        self.height = sy*self.image.height
        self.scale.scaleFactor.setValue(sx,sy,1.0)
    
 
    def getDisplayModes(self,obj):
        "'''Return a list of display modes.'''"
        modes=[]
        modes.append("Shaded")
        modes.append("Wireframe")
        return modes
 
    def getDefaultDisplayMode(self):
        "'''Return the name of the default display mode. It must be defined in getDisplayModes.'''"
        return "Shaded"
 
    def setDisplayMode(self,mode):
        return mode
 
    def onChanged(self, vp, prop):
        #FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
        if prop=="Transparency" :
            t = vp.getPropertyByName("Transparency")
            t=min(max(t,0),100)
            self.material.transparency.setValue(t/100)
 
    def getIcon(self):
        return """
            /* XPM */
            static const char * ViewProviderBox_xpm[] = {
            "16 16 6 1",
            "   c None",
            ".  c #141010",
            "+  c #615BD2",
            "@  c #C39D55",
            "#  c #000000",
            "$  c #57C355",
            "        ........",
            "   ......++..+..",
            "   .@@@@.++..++.",
            "   .@@@@.++..++.",
            "   .@@  .++++++.",
            "  ..@@  .++..++.",
            "###@@@@ .++..++.",
            "##$.@@$#.++++++.",
            "#$#$.$$$........",
            "#$$#######      ",
            "#$$#$$$$$#      ",
            "#$$#$$$$$#      ",
            "#$$#$$$$$#      ",
            " #$#$$$$$#      ",
            "  ##$$$$$#      ",
            "   #######      "};
            """
 
    def __getstate__(self):
        return None
 
    def __setstate__(self,state):
        return None
 
 
def makeImagePlane(im2=None):
    a=FreeCAD.ActiveDocument.addObject("Part::Part2DObjectPython","ImagePlane")
    ImagePlane(a, im2)
    ViewProviderImagePlane(a.ViewObject, im2)
    pl = FreeCAD.Placement()
    pl.Rotation = FreeCADGui.ActiveDocument.ActiveView.getCameraOrientation()
    pl.Base = FreeCAD.Vector(0.0,0.0,0.0)
    a.Placement=pl
    FreeCAD.ActiveDocument.recompute()
    

