import FreeCADGui, FreeCAD, Part
import math
import pivy.coin as pvy
from PySide import QtCore, QtGui
import DraftTrackers, Draft

def distance(p1,p2):
    dx=p2[0]-p1[0]
    dy=p2[1]-p1[1]
    dz=p2[2]-p1[2]
    return math.sqrt(dx*dx+dy*dy+dz*dz)
    

class ScalePlane():

    def __init__(self, view):
        self.view = view
        self.stack = []
        self.impl=None
        self.callback = self.view.addEventCallbackPivy(pvy.SoMouseButtonEvent.getClassTypeId(),self.getpoint)
        self.callmouse=self.view.addEventCallbackPivy(pvy.SoLocation2Event.getClassTypeId(),self.getmousepoint)
        self.distance=0
        self.form=QtGui.QWidget()
        self.label = QtGui.QLabel(self.form)
        self.label.setGeometry(QtCore.QRect(30, 10, 66, 17))
        self.lineEdit = QtGui.QLineEdit(self.form)
        self.lineEdit.setGeometry(QtCore.QRect(100, 10, 113, 29))
        self.label1 = QtGui.QLabel(self.form)
        self.label1.setGeometry(QtCore.QRect(20, 45, 260, 17))
        self.label.setText("Distance")
        self.label1.setText("Select first point")
        self.tracker = DraftTrackers.lineTracker(scolor=(1,0,0))
        self.tracker.raiseTracker()
        self.tracker.on()
        FreeCADGui.Control.showDialog(self)

        
    def accept(self):
        try:
            obj = FreeCAD.ActiveDocument.getObject(self.impl['Object'])
            locale=QtCore.QLocale.system()
            d, ok = locale.toFloat(self.lineEdit.text())
            if not ok:
                raise ValueError
            s=d/self.distance
            obj.xScale=s
            obj.yScale=s
            FreeCAD.Console.PrintMessage("Scale="+str(s))
            self.tracker.off()
            self.tracker.finalize()
            FreeCADGui.Control.closeDialog(self)
        except ValueError, ZeroDivisionError:
            self.label1.setText("<font color='red'>Enter distance</font>")
            return
        except IndexError, AttributeError:
            self.label1.setText("<font color='red'>Select ImagePlane</font>")
            return
        
    def reject(self):
        self.stack=[]
        self.view.removeEventCallbackPivy(pvy.SoMouseButtonEvent.getClassTypeId(),self.callback)
        self.view.removeEventCallbackPivy(pvy.SoLocation2Event.getClassTypeId(),self.callmouse)
        self.tracker.off()
        self.tracker.finalize()
        FreeCADGui.Control.closeDialog(self)
    
    def getmousepoint(self, event_cb):
        event = event_cb.getEvent()
        if len(self.stack)==1:
            pos = event.getPosition()
            point = self.view.getPoint(pos[0],pos[1])
            self.tracker.p2(point)
               
    def getpoint(self,event_cb):
        event = event_cb.getEvent()           
        if event.getState() == pvy.SoMouseButtonEvent.DOWN:
            pos = event.getPosition()
            if self.impl==None :
                self.impl = self.view.getObjectInfo((pos[0],pos[1]))
                print self.impl
            point = self.view.getPoint(pos[0],pos[1])
            self.stack.append(point)
            self.label1.setText("Select second point")
            if len(self.stack)==1:
                self.tracker.p1(point)
            elif len(self.stack) == 2:
                self.distance=distance(self.stack[0], self.stack[1])
                self.tracker.p2(point)
                self.view.removeEventCallbackPivy(pvy.SoMouseButtonEvent.getClassTypeId(),self.callback)
                self.view.removeEventCallbackPivy(pvy.SoLocation2Event.getClassTypeId(),self.callmouse)
                self.label1.setText("Select Image Plane and type distance")
                
def setScale():            
    v=FreeCADGui.activeDocument().activeView()
    ScalePlane(v)
    FreeCAD.ActiveDocument.recompute()       
