import FreeCAD, FreeCADGui
from pivy import coin

class ImagePlane:
    def __init__(self, obj, image2):
        self.image=image2
        obj.addProperty("App::PropertyFloat","xScale","ImagePlane","X scale of the image plane").xScale=1.0
        obj.addProperty("App::PropertyFloat","yScale","ImagePlane","Y scale of the image plane").yScale=1.0
        obj.Proxy = self
   
    def onChanged(self, fp, prop):
        "'''Do something when a property has changed'''"
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
 
    def execute(self, fp):
        "'''Do something when doing a recomputation, this method is mandatory'''"
        FreeCAD.Console.PrintMessage("Recompute\n")
 
class ViewProviderImagePlane:
    def __init__(self, obj, image2):
        obj.addProperty("App::PropertyColor","Color","ImagePlane","Color of the plane").Color=(1.0,1.0,1.0)
        obj.addProperty("App::PropertyFloat","Transparency","ImagePlane","Transparency in %").Transparency=0.0
        self.image=image2
        self.width=self.image.width
        self.height=self.image.height
        obj.Proxy = self
 
    def attach(self, obj):
        "'''Setup the scene sub-graph of the view provider, this method is mandatory'''"
        self.shaded = coin.SoGroup()
        self.wireframe = coin.SoGroup()
        self.scale = coin.SoScale()
        self.material=coin.SoMaterial()
        self.color = coin.SoBaseColor()
        self.material.transparency.setValue(obj.Transparency/100)
        self.material.emissiveColor.setValue(coin.SbColor(1,1,1))
        
        ipVertexes = coin.SoVertexProperty()

        # Define the square's spatial coordinates
        ipVertexes.vertex.set1Value(0, coin.SbVec3f(-self.width/2, -self.height/2, 0))
        ipVertexes.vertex.set1Value(1, coin.SbVec3f( self.width/2, -self.height/2, 0))
        ipVertexes.vertex.set1Value(2, coin.SbVec3f( self.width/2,  self.height/2, 0))
        ipVertexes.vertex.set1Value(3, coin.SbVec3f(-self.width/2,  self.height/2, 0))

        # Define the square's normal
        ipVertexes.normal.set1Value(0, coin.SbVec3f(0, 0, 1))

        # Define the square's texture coordinates
        ipVertexes.texCoord.set1Value(0, coin.SbVec2f(0, 0))
        ipVertexes.texCoord.set1Value(1, coin.SbVec2f(1, 0))
        ipVertexes.texCoord.set1Value(2, coin.SbVec2f(1, 1))
        ipVertexes.texCoord.set1Value(3, coin.SbVec2f(0, 1))

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
        self.onChanged(obj,"Color")
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
        "'''Here we can do something when a single property got changed'''"
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
        if prop == "Color":
            c = vp.getPropertyByName("Color")
            self.color.rgb.setValue(c[0],c[1],c[2])
        elif prop=="Transparency" :
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
    a=FreeCAD.ActiveDocument.addObject("App::FeaturePython","ImagePlane")
    ImagePlane(a, im2)
    ViewProviderImagePlane(a.ViewObject, im2)
