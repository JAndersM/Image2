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

class PointMover:
   def __init__(self, view):
       self.view = view
       self.first=True
       self.planepoint=None
       self.callback=self.view.addEventCallbackPivy(pvy.SoMouseButtonEvent.getClassTypeId(),self.positionOrigo)
       self.panel = PointPanel()
       FreeCADGui.Control.showDialog(self.panel)
       
   
   def positionOrigo(self, event_cb):
       event = event_cb.getEvent()
       if event.getState() == pvy.SoMouseButtonEvent.DOWN :
           pos = event.getPosition()
           info = self.view.getObjectInfo((pos[0],pos[1]))
           if self.first :
               try:
                   self.planepoint=[info['x'],info['y'],info['z']]
                   self.first=False
                   self.panel.label.setText("Click on image plane point")
               except TypeError:
                   pass
           else:
               try:
                   if info['Object'][:10] =='ImagePlane':
                       pl = FreeCAD.ActiveDocument.getObject(info['Object']).Placement
                       pl.move(FreeCAD.Vector(self.planepoint[0]-info['x'],self.planepoint[1]-info['y'],self.planepoint[2]-info['z']))
                       FreeCAD.ActiveDocument.getObject(info['Object']).Placement = pl
                       self.view.removeEventCallbackPivy(pvy.SoMouseButtonEvent.getClassTypeId(),self.callback)
                       FreeCADGui.Control.closeDialog(self.panel)
               except TypeError:
                   pass    

class PointPanel:

    def __init__(self):
        self.setupUI()
        
    def setupUI(self):
        self.form=QtGui.QWidget()
        self.label = QtGui.QLabel(self.form)
        self.label.setGeometry(QtCore.QRect(10, 10, 200, 17))
        self.label.setText("Click on target point") 
                
def setOrigo():
    v=FreeCADGui.activeDocument().activeView()
    OrigoMover(v)

def setPoint():
    v=FreeCADGui.activeDocument().activeView()
    PointMover(v)
                         

