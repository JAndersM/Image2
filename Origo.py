import FreeCAD, FreeCADGui, Draft
import pivy.coin as pvy

class OrigoMover:
   def __init__(self, view):
       self.view = view
       self.callback=self.view.addEventCallbackPivy(pvy.SoMouseButtonEvent.getClassTypeId(),self.positionOrigo)
   
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


def setOrigo():
    v=FreeCADGui.activeDocument().activeView()
    o = OrigoMover(v)
                         

