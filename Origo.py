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
           if info['Object'][:10] =='ImagePlane':
               Draft.move(FreeCAD.ActiveDocument.getObject(info['Object']),FreeCAD.Vector(-info['x'],-info['y'],-info['z'])) 
           FreeCAD.Console.PrintMessage("Object info: " + str(info) + "\n")
           self.view.removeEventCallbackPivy(pvy.SoMouseButtonEvent.getClassTypeId(),self.callback)




def setOrigo():
    v=FreeCADGui.activeDocument().activeView()
    o = OrigoMover(v)
    
#v=Gui.ActiveDocument.ActiveView
#p=v.getCursorPos()
#v.getObjectInfo(p)                        
#{'Document': 'Unnamed', 'Object': 'ImagePlane', 'Component': '', 'y': -60.431907653808594, 'x': 17.05440902709961, 'z': 0.0}
#v.getObjectInfo(p)['Object']
