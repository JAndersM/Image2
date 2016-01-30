import FreeCAD, FreeCADGui
from pivy import coin
from PySide import QtGui

class Image2:
    def __init__(self, obj, imfilename):
        self.image=QtGui.QImage()
        self.image.load(imfilename)
        self.filename=imfilename
        self.width=self.image.width()
        self.height=self.image.height()
        obj.addProperty("App::PropertyString","ImageFile","Image","Image file").ImageFile=self.filename
        obj.addProperty("App::PropertyInteger","Width","Image","Width of the image").Width=self.width
        obj.addProperty("App::PropertyInteger","Height","Image","Height of the image").Height=self.height
        obj.Proxy = self
        
    def getTexture(self):
        tex = coin.SoTexture2()
        tex.filename = str(self.filename)
        return tex
   
    def onChanged(self, fp, prop):
        "'''Do something when a property has changed'''"
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
 
    def execute(self, fp):
        "'''Do something when doing a recomputation, this method is mandatory'''"
        FreeCAD.Console.PrintMessage("Recompute\n")
        
class ViewProviderImage2:
    def __init__(self, obj):
        "'''Set this object to the proxy object of the actual view provider'''"
        obj.Proxy = self
 
    def attach(self, obj):
        "'''Setup the scene sub-graph of the view provider, this method is mandatory'''"
        return
 
    def updateData(self, fp, prop):
        "'''If a property of the handled feature has changed we have the chance to handle this here'''"
        # fp is the handled feature, prop is the name of the property that has changed
        return

 
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

def makeImage2():
    jpgfilename = QtGui.QFileDialog.getOpenFileName(QtGui.qApp.activeWindow(),'Open image file','*.jpg')
    a=FreeCAD.ActiveDocument.addObject("App::FeaturePython","Image")
    im2=Image2(a, jpgfilename[0])
    ViewProviderImage2(a.ViewObject)
    return im2
    
