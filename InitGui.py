import image2_rc
    
class Image2Workbench ( Workbench ):
    "Image2 workbench object"
    Icon = ":/Icons/Im2_ImagePlane.svg"
    MenuText = "Image2"
    ToolTip = "Python Image workbench"

    def GetClassName(self):
        return "Gui::PythonWorkbench"

    def Initialize(self):
        import Commands
        self.appendToolbar("Image2 Tools", ["ImportImage"])
        self.appendToolbar("Image2Plane Tools", ["CreateImagePlane", "MoveOrigo", "ToggleTransparency"])
        self.appendMenu("Image2 Tools", ["ImportImage", "CreateImagePlane", "MoveOrigo", "ToggleTransparency"])
        Log ("Loading Image2... done\n")

    def Activated(self):
        # do something here if needed...
        Msg ("Image2.Activated()\n")

    def Deactivated(self):
        # do something here if needed...
        Msg ("Image2.Deactivated()\n")
        
FreeCADGui.addWorkbench(Image2Workbench)
