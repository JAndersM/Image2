import FreeCAD, FreeCADGui, Draft
import pivy.coin as pvy
from PySide import QtGui,QtCore

class OrigoMover:
   def __init__(self, view):
       self.view = view
       self.callback=self.view.addEventCallbackPivy(pvy.SoMouseButtonEvent.getClassTypeId(),self.positionOrigo)
       self.panel = OriginPanel()
       FreeCADGui.Control.showDialog(self.panel)
       
   
   def positionOrigo(self, event_cb):
       event = event_cb.getEvent()
       if event.getState() == pvy.SoMouseButtonEvent.DOWN :
           pos = event.getPosition()
           info = self.view.getObjectInfo((pos[0],pos[1]))
           try:
               if info['Object'][:10] =='ImagePlane':
                   pl = FreeCAD.ActiveDocument.getObject(info['Object']).Placement
                   pl.move(FreeCAD.Vector(-info['x'],-info['y'],-info['z']))
                   FreeCAD.ActiveDocument.getObject(info['Object']).Placement = pl
               #FreeCAD.Console.PrintMessage("Object info: " + str(info) + "\n")
           except TypeError:
               pass
           self.view.removeEventCallbackPivy(pvy.SoMouseButtonEvent.getClassTypeId(),self.callback)
           FreeCADGui.Control.closeDialog(self.panel)

class OriginPanel:

    def __init__(self):
        self.setupUI()
        
    def setupUI(self):
        self.form=QtGui.QWidget()
        self.label = QtGui.QLabel(self.form)
        self.label.setGeometry(QtCore.QRect(10, 10, 200, 17))
        self.label.setText("Click on point to set to origo")          
        
    #def accept(self):
    #    FreeCAD.Console.PrintMessage("Run this code after a click on OK\n")
    #    return True

    #def reject(self):
    #    FreeCAD.Console.PrintMessage("Run this code after a click on Cancel\n")
    #    return True

def setOrigo():
    v=FreeCADGui.activeDocument().activeView()
    o = OrigoMover(v)
                         

