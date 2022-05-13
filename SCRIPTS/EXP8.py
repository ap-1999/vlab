from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLCDNumber, QAbstractSpinBox, QMessageBox, QSizePolicy, QDial, QVBoxLayout, QDoubleSpinBox, QLabel, QGridLayout,QLineEdit, QPushButton,QGroupBox, QHBoxLayout

import random
from ModWidgets import Dial, PushButton, TableMod, VoHGroup, VoHWidget, VolSlider
from common import EXP_PAGE, ImageLabel
from DragNDrop import DragLabel, DropLabel
import cmath
import math

class Exp8_class(EXP_PAGE):
    def __init__(self, stack):
        imageList = [0, 0, 0]
        for i in [0, 1, 2]:
            imageList[i] = "media/id-"+str(i+1)+".jpg"
        #self.dataGEN=[0, 0, 0]
        super().__init__(imageList, "media/exp4.mp4", stack)

        #setup table rack for chemicals
        self.SolsTab = TableMod(10, 7)
        self.setUPtable()
        
        #setup titration
        self.TitDrop = DropLabel("Bur", "media/test_bg.png",self)
        self.TitDrop.textChanged.connect(self.update2)

        self.FlaDrop = ImageLabel("Flask", "media/water_bath.png", self)
        

        self.OnButt = PushButton("-RESET-")
        self.HOTBUTT = PushButton("-HOT BATH-")
        self.HOTBUTT.clicked.connect(self.TURNON)
        self.COLDBUTT = PushButton("-COLD BATH-")

        self.UnknownComp = DragLabel("Unk", "media/smallflask.jpg",False, self)
        self.UnknownCompLab = ImageLabel("UNKNOWN COMP")
        
        self.ButtLay = VoHGroup('V')
        self.ButtLay.addWidgets([self.OnButt, self.HOTBUTT, self.COLDBUTT])
        self.COMP = VoHGroup('V')
        self.COMP.addWidgets([self.UnknownComp, self.UnknownCompLab])

        self.MISC = VoHWidget('H')
        self.MISC.addWidgets([self.COMP,self.ButtLay])
        #self.MISC.setMaximumHeight()
        #self.movie = VolSlider()

        self.reset2 = QPushButton("Reset")
        #self.reset2.clicked.connect(self.RESET2)
        
        self.DROP2 = VoHGroup("V")
        self.DROP2.addWidgets([self.TitDrop.getLabel(), self.FlaDrop])

        self.LEFTSIDE = VoHWidget('V')
        self.LEFTSIDE.addWidgets([self.DROP2, self.MISC])

        self.loadNAOH = PushButton("Load NaOH")
        #self.loadNAOH.clicked.connect(self.LoadHypo)
        
        self.loadStart = PushButton("START")
        #self.loadStart.clicked.connect(self.START2)
        self.loadStop = PushButton("PAUSE")
        #self.loadStop.clicked.connect(self.Pause)
        self.loadRe = PushButton("RESET")
        #self.loadRe.clicked.connect(self.RESET2)

        self.func_grp=0
        self.func_acid=0
        self.func_carb=0
        self.func_carb_1=0
        self.func_starch=0
        self.func_carbonyl=0
        self.gen_compound()


        #self.phDisplay = ImageLabel(" MORE TO ADD HERE")

        self.Side1W=VoHWidget("H")
        self.Side1W.addWidgets([self.LEFTSIDE, self.SolsTab])
        self.Page4lay = QHBoxLayout()
        self.Page4lay.addWidget(self.Side1W)
        self.UNKNOWNLOAD = False
        self.dropCount=0

        self.tab2.setLayout(self.Page4lay)

        self.DROPLIST = set()
        self.errorMessage=0

        print(self.func_grp)
        self.WATERBATH = 'OFF'
    def gen_compound(self):
        self.func_grp=random.randint(0, 2)
        self.func_acid=random.randint(0, 1)
        self.func_carb=random.randint(0, 1)
        self.func_carb_1=random.randint(0, 1)
        self.func_starch=random.randint(0, 1)
        self.func_carbonyl=random.randint(0, 1)

    def TURNON(self):
        if (self.HOTBUTT.text() == 'HOT') and (self.COLDBUTT.text() == 'COLD'):
            self.WATERBATH='HOT'
            self.HOTBUTT.setText('TURN_OFF')
        if (self.HOTBUTT.text() == 'TURN_OFF'):
            self.WATERBATH='OFF'
            self.HOTBUTT.setText('HOT')
        
    def TURNCOLD(self):
        if (self.HOTBUTT.text() == 'HOT') and (self.COLDBUTT.text() == 'COLD'):
            self.WATERBATH='COLD'
            self.COLDBUTT.setText('TURN_OFF')
        if (self.HOTBUTT.text() == 'TURN_OFF'):
            self.WATERBATH='OFF'
            self.COLDBUTT.setText('COLD')


    def setUPtable(self):
        names = ["Sols->", " NaHCO3 ", " AgNO3 ", " RESORCINOL ", " conc. H2SO4 ", " NaOH ", " H₂O "]
        names1 = ["Sols->"," α-NAPHTHOL ", " FEHLING A ", " FEHLING B ", " conc. HCl ", " dil I2 ", " 2,4-DNP "]
        for i in range(7) :
            self.SolsTab.setCellWidget(0, i, ImageLabel(names[i]))

            if(i):
                self.SolsTab.setCellWidget(3, i, DragLabel(names[i], "media/light2.png", False, self))
                self.SolsTab.setCellWidget(4, i, QDoubleSpinBox())
                #self.SolsTab.cellWidget(4, i).valueChanged.connect(self.VolEntry)
                temp2 = ImageLabel("")
                temp2.setFont(QFont('Times'))
                self.SolsTab.setCellWidget(1, i, temp2)
                self.SolsTab.setCellWidget(2, i, QDoubleSpinBox())
                self.SolsTab.cellWidget(2, i).setReadOnly(True)
            else:
                self.SolsTab.setCellWidget(1, i, ImageLabel("Conc->"))
                self.SolsTab.setCellWidget(2, i, ImageLabel("Vol->"))
                self.SolsTab.setCellWidget(3, i, ImageLabel("Flask->"))
                self.SolsTab.setCellWidget(4, i, ImageLabel("Vol Taken (ml)->"))

        for i in range(7) :
            self.SolsTab.setCellWidget(5, i, ImageLabel(names1[i]))

            if(i):
                self.SolsTab.setCellWidget(8, i, DragLabel(names1[i], "media/light2.png", False, self))
                self.SolsTab.setCellWidget(9, i, QDoubleSpinBox())
                #self.SolsTab.cellWidget(9, i).valueChanged.connect(self.VolEntry)
                temp2 = ImageLabel("")
                temp2.setFont(QFont('Times'))
                self.SolsTab.setCellWidget(6, i, temp2)
                self.SolsTab.setCellWidget(7, i, QDoubleSpinBox())
                self.SolsTab.cellWidget(7, i).setReadOnly(True)
            else:
                self.SolsTab.setCellWidget(6, i, ImageLabel("Conc->"))
                self.SolsTab.setCellWidget(7, i, ImageLabel("Vol->"))
                self.SolsTab.setCellWidget(8, i, ImageLabel("Flask->"))
                self.SolsTab.setCellWidget(9, i, ImageLabel("Vol Taken (ml)->"))
        self.SolsTab.resizing()

    def update2(self):
        try:
            if(self.TitDrop.text() == "Bur"):
                return
            if(self.UNKNOWNLOAD and self.TitDrop.name() == 'Unk'):
                pass

            else:
                 
                if(self.TitDrop.name() == "Unk"):
                    pass
                PASS = False
                if(PASS == False):   
                    self.dropCount += 1
                    if(self.dropCount == 1):
                        self.TitDrop.setImage("media/t1.png")
                        self.DROPLIST.add(self.TitDrop.name())
                        
                    elif(self.dropCount == 2):
                        if(self.TitDrop.name() in self.DROPLIST):
                            self.dropCount -= 1
                        else:
                            self.TitDrop.setImage("media/t2.png")
                            self.DROPLIST.add(self.TitDrop.name())
                        if('Unk' in self.DROPLIST):
                            if (self.func_grp == 0) and (" H₂O " in self.DROPLIST )and (" NaHCO3 " in self.DROPLIST):
                                self.TitDrop.setImage("media/t2.png")
                            elif (self.func_grp==2) and (self.func_carb==1) and (self.func_carb_1== 1) and (" dil I2 " in self.DROPLIST):
                                self.TitDrop.setImage("media/starch.png")

                            elif (self.func_grp == 1) and (" 2,4-DNP " in self.DROPLIST):
                                self.TitDrop.setImage("media/dnp.png")
                            elif (self.func_grp==0) and (" AgNO3 " in self.DROPLIST):
                                self.TitDrop.setImage("media/tollen.png")
                        
                    elif(self.dropCount == 3):
                        if(self.TitDrop.name() in self.DROPLIST):
                            self.dropCount -= 1
                        else:
                            self.TitDrop.setImage("media/t3.png")
                            self.DROPLIST.add(self.TitDrop.name())

                        if('Unk' in self.DROPLIST):
                            
                            if (self.func_grp==1) and (" H₂O " in self.DROPLIST )and (self.func_carb == 0) and (" conc. H2SO4 " in self.DROPLIST) and (" α-NAPHTHOL " in self.DROPLIST):
                                self.TitDrop.setImage("media/napthol.png")

                            elif(self.func_grp==1) and (self.func_carb == 1) and (" FEHLING A " in self.DROPLIST) and (" FEHLING B " in self.DROPLIST):
                                self.TitDrop.setImage("media/fehling.png")
                            elif (self.func_grp==1) and (self.func_carb == 0) and (self.func_carb_1== 0) and (" conc. HCl " in self.DROPLIST) and (' RESORCINOL ' in self.DROPLIST):
                                self.TitDrop.setImage("media/reso.png")
                            elif (self.func_grp==1) and (self.func_carb == 0) and (self.func_carb_1 == 1) and (" conc. HCl " in self.DROPLIST) and (' RESORCINOL ' in self.DROPLIST):
                                self.TitDrop.setImage("media/pink_test.png")
                                
                    elif(self.dropCount == 4):
                        if(self.TitDrop.name() in self.DROPLIST):
                            self.dropCount -= 1
                        else:
                            self.TitDrop.setImage("media/t4.png")
                            self.DROPLIST.add(self.TitDrop.name())
                        if('Unk' in self.DROPLIST):
                            if (self.func_grp==0) and (self.func_acid == 1) and (" conc. H2SO4 " in self.DROPLIST) and (" NaOH " in self.DROPLIST) and (' RESORCINOL ' in self.DROPLIST):
                                self.TitDrop.setImage("media/fluro.png")
                        #self.EquiLab.setStyleSheet("QLineEdit {color: none; background-image : url(media/l4test.png); background-repeat: no-repeat;background-position: 0% 0%;}")
                    else:
                        self.errorFlag = 5
                        self.errorMessage()

            self.TitDrop.setText("Bur")
            
        except Exception as e :
            print(e)
            #self.UNKNOWNERROR = "Updating Flask parameters "+str(e)
            self.errorMessage()
            self.TitDrop.setText("Bur")


    def errorMessage(self):
        self.w = QMessageBox()
        self.w.resize(150, 150)
        self.UNKNOWNERROR = "Unidentified"
        title  = "Unknown Error"
        text = "Unidentified error. Try reset or restarting the program.Report a bug.\nPotential Error:>" + self.UNKNOWNERROR
        textMain ="Instrument Error!"
        
        if(self.errorFlag == 1):
            text = "Please Enter the Volume within the available Amount"
            textMain = "Volume taken exceeds max vol available"
            title = "VOLUME UNAVAILABLE ERROR"
        elif(self.errorFlag == 2):
            title  = "ONGOING REACTION ERROR"
            text = "Previous reaction is already in progess. Reset and try again."
            textMain ="Reaction in progress"
        elif(self.errorFlag == 3):
            title = "EXTRA COMPONENTS ERROR"
            text = "Reset recommended. Extra components are present, which will hamper reaction and equilibrium"
            textMain ="Extra components in test tube."
        elif(self.errorFlag == 4):
            text = "Some Components are missing from the reaction mixture. Plese reverify and try again."
            textMain = "Missing Components"
            title = "ERROR"
        elif(self.errorFlag == -1):
            text = "Indicator is missing from the reaction mixture. Plese add indicator."
            textMain = "Missing Indicator"
            title = "NO INDICATOR"
        elif(self.errorFlag == -2):
            text = "Titrant is missing from the Flask. Plese Drag and drop a Titrant."
            textMain = "Missing Solution"
            title = "NO TITRANT"

        elif(self.errorFlag == 5):
            text = "Warning! Exceeding test tube volume. No More solutions can be added."
            textMain = "Overflow !"
            title = "ATTENTION Overflow"
        elif(self.errorFlag == 6):
            text = "ATTENTION !! Reaction in Flask will now start. Please keep your Timer handy."
            title = "ATTENTION ! Reaction start"
            textMain = "REACTION START"
        elif(self.errorFlag == 7):
            text = "ATTENTION !! Nothing is Loaded. Drag and drop a Flask."
            title = "ATTENTION ! Empty Test tube"
            textMain = "EMPTY Test tube"
            
        elif(self.errorFlag == 8):
            text = "ATTENTION !!This solution is already loaded. Load another sample or Reset"
            title = "ATTENTION ! Solution Loaded"
            textMain = "Solution is already loaded."
        elif(self.errorFlag == 9):
            text = "ATTENTION !! Reaction in Flask has reached it's end. You May retrieve your solution."
            title = "ATTENTION ! Reaction COMPLETE"
            textMain = "REACTION COMPLETE"
            
        elif(self.errorFlag == 10):
            text = "Please add NaOH in burette. It is preffered that NaOH is added in Burrete instead of any other solution ."
            textMain = "NaOH preffered in burette"
            title = "Attention !"
            
        elif(self.errorFlag == 11):
            text = "The Solution added is not titrable. Please reverify and add another solution in flask."
            textMain = "Non titrable solution added"
            title = "Attention !"

        elif(self.errorFlag == 12):
            title = "NaOH"
            text = "Warning! Load NaOH in Burrete to Resume. Load and then Resume"
            textMain = "LOAD NaOH"

        elif(self.errorFlag == 13):
            title = "Calibration"
            text = "Successfully calibrated !!!"
            textMain = "Calibration Completed"

        if(self.errorFlag >= 5):
            self.w.setIcon(QMessageBox.Information)
        else:
            self.w.setIcon(QMessageBox.Critical)
        self.w.setText(textMain)
        self.w.setInformativeText(text)
        self.w.setWindowTitle(title)
        self.w.exec()
        self.errorFlag = 0
        self.UNKNOWNERROR = "Unidentified"