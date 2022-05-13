from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout,QLCDNumber,QMessageBox, QDoubleSpinBox, QWidget, QLabel,QLineEdit, QPushButton, QHBoxLayout
import random
from ModWidgets import Dial, FGroup, TableMod, VoHGroup, VoHWidget, PushButton
from DragNDrop import DragLabel, DropLabel
from common import EXP_PAGE, ImageLabel

import matplotlib
import matplotlib.animation as animation

from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure
from matplotlib import style

LARGE_FONT= QFont("Verdana", 12)
style.use("ggplot")

ab = open('Logs/Data_input.txt', 'w')
ab.write('')
ab.close()

f2 = Figure(figsize=(20,20), dpi=100)
a3 = f2.add_subplot(111)

def animate2(self):
        pullData3 = open("Logs/Data_input.txt", 'r').read()
        dataList3 = pullData3.split('\n')
        xlist3 = []
        ylist3 = []
        x3 = ''
        y3 = ''
        for eachLine in dataList3 :
            if len(eachLine)!=0:
                x3, y3 = eachLine.split()
                try:
                    x31 = "%.2f"%(float(x3))
                    y31 = "%.2f"%(float(y3))
                    xlist3.append(float(x31))
                    ylist3.append(float(y31))
                except:
                    pass

        a3.clear()
        try:
            a3.plot(xlist3, ylist3, label =(str("%.2f"%(float(x3)))+'min\n'+ str("%.2f"%(float(y3)))+'uScm-1'))
            a3.legend(loc= 'upper right', bbox_to_anchor=(1.1,1.105), ncol=3, fancybox=True, shadow=True)
        except:
            pass
        a3.set_title("UV_VIS")
        a3.set_ylabel('ABSORBANCCE')
        a3.set_xlabel('Lambda')



class Exp9_class(EXP_PAGE):
    def __init__(self, stack):
        imageList = [0, 0, 0]
        for i in [0, 1, 2]:
            imageList[i] = "media/uv-"+str(i+1)+".jpg"
        #self.dataGEN=[0, 0, 0]
        super().__init__(imageList, "media/exp4.mp4", stack)

        #setup table rack for chemicals
        self.SolsTab = TableMod(5, 7)
        self.setUPtable()

        self.meterLabel = DropLabel("Drop_here", 'media/uv_open.jpg', self)#CHANGE IMAGE TO UV VIS
        self.meterLabel.textChanged.connect(self.update)

        self.canvas3 = FigureCanvas(f2)
        self.Tb3 = NavigationToolbar(self.canvas3, self)

        self.Group6o = QGroupBox()
        self.tempF26o = QVBoxLayout()
        self.tempF26o.addWidget(self.canvas3)
        self.tempF26o.addWidget(self.Tb3)

        self.ani2 = animation.FuncAnimation(f2, animate2, interval=1000)

        





    def setUPtable(self):
        names = ["Sols->", "Benzene", "Benzoic Acid(BA)", "4-amino BA (ABA)", "BA in NaOH", "ABA in NaOH", "BA in HCl", "4-ABA in HCl"]
        for i in range(8) :
            self.SolsTab.setCellWidget(0, i, ImageLabel(names[i]))

            if(i):
                self.SolsTab.setCellWidget(3, i, DragLabel(names[i], "media/light2.png", True, self))
                self.SolsTab.setCellWidget(4, i, QDoubleSpinBox())
                self.SolsTab.cellWidget(4, i).valueChanged.connect(self.VolEntry)
                temp2 = ImageLabel(" - ")
                temp2.setFont(QFont('Times'))
                self.SolsTab.setCellWidget(1, i, temp2)
                self.SolsTab.setCellWidget(2, i, QDoubleSpinBox())
                self.SolsTab.cellWidget(2, i).setReadOnly(True)
            else:
                self.SolsTab.cellWidget(2, 1).setValue(12)
                self.SolsTab.setCellWidget(1, i, ImageLabel("Conc->"))
                self.SolsTab.setCellWidget(2, i, ImageLabel("Vol->"))
                self.SolsTab.setCellWidget(3, i, ImageLabel("Flask->"))
                self.SolsTab.setCellWidget(4, i, ImageLabel("Vol Taken (ml)->"))
                
        self.SolsTab.resizing()

    def VolEntry(self):
        column = self.SolsTab.currentColumn()
        val = self.SolsTab.cellWidget(4, column).value()
        valAva = self.SolsTab.cellWidget(2, column).value()
        if(val > valAva):
            self.errorFlag = 1
            self.errorMessage()
            self.SolsTab.cellWidget(4, column).setValue(0)
            return
        #valAva = valAva-val
        #self.SolsTab.cellWidget(2, column).setValue(valAva)
        self.SolsTab.cellWidget(3, column).setVol(val)