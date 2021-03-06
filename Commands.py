import FreeCAD,FreeCADGui
from PySide import QtCore, QtGui
 
class ImportImageCommand:
    "Import image from file"
    def GetResources(self):
        return {"MenuText": "Import image",
                "Accel": "Ctrl+M",
                "ToolTip": "Imports an image",
                "Pixmap"  : ":/Icons/Im2_importImage.svg"}
 
    def IsActive(self):
        return True
 
    def Activated(self):
        if FreeCAD.ActiveDocument == None:
            FreeCAD.newDocument()
        import Image2
        Image2.makeImage2()

class ImagePlaneCommand:
    "Creates image plane"
    def GetResources(self):
        return {"MenuText": "Create image plane",
                "Accel": "Ctrl+M",
                "ToolTip": "Creates image plane from selected image",
                "Pixmap"  : ":/Icons/Im2_ImagePlane.svg"}
 
    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
            return False
        else:
            return True
 
    def Activated(self):
        sel=FreeCADGui.Selection.getSelection()
        try :
            imfile=sel[0].ImageFile #Do we have an image file
            import ImagePlane
            ImagePlane.makeImagePlane(sel[0].Proxy)
        except IndexError, AttributeError:
            diag = QtGui.QMessageBox(QtGui.QMessageBox.Warning, 'Can not create image plane', "Select an image first.")
            diag.setWindowModality(QtCore.Qt.ApplicationModal)
            diag.exec_()
            return
        
class PlaneTransCommand:
    "Toggles image plane transparency"
    def GetResources(self):
        return {"MenuText": "Toggle transparency",
                "Accel": "Ctrl+M",
                "ToolTip": "Toggle 50% transparency for image plane",
                "Pixmap"  : ":/Icons/Im2_50Trans.svg"}
 
    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
            return False
        else:
            return True
 
    def Activated(self):
        sel=FreeCADGui.Selection.getSelection()
        try :
            sel[0].ViewObject.Transparency=50-sel[0].ViewObject.Transparency
        except IndexError, AttributeError:
            return

class PlaneOrigoCommand:
    "Moves selected point to origo"
    def GetResources(self):
        return {"MenuText": "Set origo",
                "Accel": "Ctrl+M",
                "ToolTip": "Click to set point to origo",
                "Pixmap"  : ":/Icons/Im2_Origo.svg"}
 
    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
            return False
        else:
            return True
 
    def Activated(self):
        import MoveImagePlane
        MoveImagePlane.setOrigo()

class PlanePointCommand:
    "Moves selected point to point on object"
    def GetResources(self):
        return {"MenuText": "Move plane to new point",
                "Accel": "Ctrl+M",
                "ToolTip": "Moves image plane to point on other object",
                "Pixmap"  : ":/Icons/Im2_Point.svg"}
 
    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
            return False
        else:
            return True
 
    def Activated(self):
        import MoveImagePlane
        MoveImagePlane.setPoint()

class ScalePlaneCommand:
    "Scales selected image plane"
    def GetResources(self):
        return {"MenuText": "Scale plane",
                "Accel": "Ctrl+M",
                "ToolTip": "Scales selected image plane",
                "Pixmap"  : ":/Icons/Im2_Scale.svg"}
 
    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
            return False
        else:
            return True
 
    def Activated(self):
        import ScaleImagePlane
        ScaleImagePlane.setScale()
               
FreeCADGui.addCommand('ImportImage',ImportImageCommand())
FreeCADGui.addCommand('CreateImagePlane',ImagePlaneCommand())
FreeCADGui.addCommand('ToggleTransparency',PlaneTransCommand())
FreeCADGui.addCommand('MoveOrigo',PlaneOrigoCommand())
FreeCADGui.addCommand('MovePoint',PlanePointCommand())
FreeCADGui.addCommand('ScalePlane',ScalePlaneCommand())
