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
    
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        self.view = FreeCADGui.ActiveDocument.ActiveView
        self.stack = []
        self.callback = self.view.addEventCallbackPivy(pvy.SoMouseButtonEvent.getClassTypeId(),self.getpoint)
        self.callmouse=self.view.addEventCallbackPivy(pvy.SoLocation2Event.getClassTypeId(),self.getmousepoint)
        self.distance=0
        self.dialog=Dialog
        Dialog.setObjectName("Dialog")
        Dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        Dialog.resize(300, 102)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(50, 70, 191, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 10, 66, 17))
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(100, 10, 113, 29))
        self.label1 = QtGui.QLabel(Dialog)
        self.label1.setGeometry(QtCore.QRect(20, 45, 260, 17))
        self.label.setText("Distance")
        self.label1.setText("Select first point")
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.tracker = DraftTrackers.lineTracker(scolor=(1,0,0))
        self.tracker.raiseTracker()
        self.tracker.on()
        self.dialog.show()

        
    def accept(self):
        sel = FreeCADGui.Selection.getSelection()
        try:
            locale=QtCore.QLocale.system()
            d, ok = locale.toFloat(self.lineEdit.text())
            if not ok:
                raise ValueError
            s=d/self.distance
            sel[0].xScale=s
            sel[0].yScale=s
            FreeCAD.Console.PrintMessage("Scale="+str(s))
            self.tracker.off()
            self.tracker.finalize()
            self.dialog.hide()
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
        self.dialog.hide()
    
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
                self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)
                self.label1.setText("Select Image Plane and type distance")
                
def setScale():            
    d = QtGui.QWidget()
    ui = Ui_Dialog()
    ui.setupUi(d)
    FreeCAD.ActiveDocument.recompute()       
