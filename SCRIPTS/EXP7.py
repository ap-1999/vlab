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

class Exp7_class(EXP_PAGE):

    def __init__(self, stack):
        imageList = [0, 0, 0, 0]
        for i in [0, 1, 2, 3]:
            imageList[i] = "media/ph-"+str(i+1)+".jpg"
        super().__init__(imageList, "media/exp4.mp4", stack)
        #setup table rack for chemicals
        self.SolsTab = TableMod(5, 6)
        self.setUPtable()
        self.dataGEN=[0, 0, 0]
        self.dataGEN[2] = 4.75
        self.dataGEN[0] = self.conc_na
        
        
        #setup titration
        self.TitDrop = DropLabel("Bur", "media/bur-min.png",self)
        self.TitDrop.textChanged.connect(self.update3)

        self.FlaDrop = DropLabel("Flask", "media/ph_pic.png", self)
        self.FlaDrop.textChanged.connect(self.update2)
        
        self.movie = VolSlider()

        self.reset2 = QPushButton("Reset")
        self.reset2.clicked.connect(self.RESET2)
        
        self.DROP2 = QGridLayout()
        self.DROP2.addWidget(self.movie, 0, 0, 3, 1)
        self.DROP2.addWidget(self.TitDrop.getLabel(), 0, 1, 1, 1)
        self.DROP2.addWidget(self.FlaDrop.getLabel(), 1, 1, 1, 1)
        self.DROP2.addWidget(self.reset2, 2, 1, 1, 1)
        self.DROP2W = QGroupBox()
        self.DROP2W.setLayout(self.DROP2)

        self.loadNAOH = PushButton("Load NaOH")
        self.loadNAOH.clicked.connect(self.LoadHypo)
        
        self.loadStart = PushButton("START")
        self.loadStart.clicked.connect(self.START2)
        self.loadStop = PushButton("PAUSE")
        self.loadStop.clicked.connect(self.Pause)
        self.loadRe = PushButton("RESET")
        self.loadRe.clicked.connect(self.RESET2)

        self.volumeDisplay = ImageLabel("0.0")
        self.volumeDisplay.setFont(QFont('Times', 30))
        self.volumeDisplay.setStyleSheet("QLabel {border : 3px solid white;}")
        #self.volumeDisplay.setReadOnly(True)

        self.volumeSpeed = Dial()
        self.volumeSpeedDis = ImageLabel("0")
        self.volumeSpeedDis.setStyleSheet("QLabel {border : 3px}")
        self.volumeSpeed.valueChanged.connect(self.changedSpeed)
        self.setUPTITBOX()

        self.CalibNob = Dial()
        self.CalibNob.valueChanged.connect(self.change_PH_display)
        self.CalibNobBut = PushButton('CALIBRATE')
        self.CalibNobBut.clicked.connect(self.CALIB_ACTION)

        self.phDisplay = ImageLabel("0.0")
        self.phDisplay.setFont(QFont('Times', 30))
        self.phDisplay.setStyleSheet("QLabel {border : 3px solid white;}")
        self.PHLAB = ImageLabel("-pH Meter Reading-")
        
        self.PHBOX = VoHGroup("V")
        self.PHBOX.addWidgets([self.phDisplay,self.PHLAB])

        self.Calib_BUTBOX = VoHGroup("V")
        self.Calib_BUTBOX.addWidgets([self.CalibNob,self.CalibNobBut])

        self.PH_ALL = VoHWidget("H")
        self.PH_ALL.addWidgets([self.Calib_BUTBOX,self.PHBOX])

        self.Side1W=VoHWidget("V")
        self.Side1W.addWidgets([self.SolsTab,self.PH_ALL])
        self.Page4lay = QHBoxLayout()
        self.Page4lay.addWidget(self.Side1W)
        self.Page4lay.addWidget(self.MISCBOX)
        self.Page4lay.addWidget(self.DROP2W)

        self.tab2.setLayout(self.Page4lay)
        
        self.errorAccu = 0
        self.errorFlag = 0
        self.flag = 0
        self.Ka = 0
        #self.Display.setText("NONE")
        self.LOADEDFLAG = False

        self.resumeFlag=False
        self.LOADMARK=-5000
        self.marker=0
        self.start=False
        self.burFlag = False
        self.loadKIFLAG= False
        self.LoadedINFLASK=False
        self.Calib_mode=False
        self.excess=False

        self.timerTrials = QTimer()
        self.timerTrials.timeout.connect(self.hiddenTimer)
        self.phon=False

        self.burVoldrop=0
        self.show_ph=0
        self.extra=1
        self.value_vol=True

    def change_PH_display(self):
        if(self.FlaDrop.name() == " Acidic Buffer " and self.LoadedINFLASK == True):
        
            changeValue = round(self.conFlask+(self.CalibNob.value()/100), 2)
            self.phDisplay.setText(str(changeValue))

    def CALIB_ACTION(self):
        try:
            if(self.FlaDrop.name() == " Acidic Buffer " and self.LoadedINFLASK == True):
                changeValue = round(self.conFlask+(self.CalibNob.value()/100), 2)
                self.extra =changeValue-4
                self.SolsTab.cellWidget(3, 3).setCon(changeValue)
                self.errorFlag = 13
                self.errorMessage()
        except Exception as e:
            self.UNKNOWNERROR = "Calibration Error> "+str(e)
            self.errorMessage()
            #self.TitDrop.setText("Bur")

    def update3(self):	
        try:
            if(self.TitDrop.text() == "Bur"):
                return
            if(self.resumeFlag):
                if(self.TitDrop.name() == " NaOH "):
                   try:
                       self.burVol = self.TitDrop.vol()
                       self.movie.setValue(int((self.burVol*100)-5000))
                       self.LOADMARK = (self.burVol*100)-5000
                       self.marker = 0
                       if(self.resumeFlag):
                           self.resumeFlag = False
                   except:
                        self.UNKNOWNERROR = "Refilling Burette through drag and drop"
                        self.errorMessage()
                   self.TitDrop.setText("Bur")
                   return
                   
                else:
                   self.errorFlag = 10
                   self.errorMessage()
                   self.TitDrop.setText("Bur") 
                   return         

            if(self.start):
                self.errorFlag = 2
                self.errorMessage()
            else:
                if(self.TitDrop.name() == " NaOH "):
                    
                    self.burCon = self.TitDrop.con()
                    self.burVol = self.TitDrop.vol()
                    self.movie.setValue(int((self.burVol*100)-5000))
                    self.LOADMARK = (self.burVol*100)-5000
                    self.burFlag = True

                else:
                    self.errorFlag = 10
                    self.errorMessage()
            self.TitDrop.setText("Bur")
        except Exception as e:
            self.UNKNOWNERROR = "Updating Burette parameters and "+str(e)
            self.errorMessage()
            self.TitDrop.setText("Bur")

    def RESET2(self):
        try:
            self.timerTrials.stop()
            self.burFlag = False
            self.start = False
            self.volFlask = 0
            self.conFlask = 0
            self.burCon = 0
            self.burVol = 0
            self.LoadedINFLASK = False
            self.volumeDown = 0
            self.marker = 0
            self.resumeFlag = False
            self.FlaDrop.setImage("media/ph_pic.png")
            #self.FlaDrop.setStyleSheet("QLineEdit {color: black; background-image : url(media/ph_pic.png); background-repeat: no-repeat;background-position: 0% 0%;}")
            self.loadKIFLAG = False
            self.RESETDROP(self.FlaDrop, "Flask")
            self.RESETDROP(self.TitDrop, "Bur")
            self.start = False
            self.loadNAOH.setEnabled(True)
            self.LOADMARK = -5000
            self.movie.setValue(-5000)
            self.timerTrials.stop()
            self.loadStop.setText("PAUSE")
            self.loadStart.setEnabled(True)
            self.loadStop.setEnabled(False)
        except:
            self.UNKNOWNERROR = "Reseting Titration parameters"
            self.errorMessage()

    def RESETDROP(self, drop, name):
        drop.setCon(0)
        drop.setVol(0)
        drop.setCol(0)
        drop.setName(name)
        drop.setText(name)

    def changedSpeed(self):
        try:
            speed = self.volumeSpeed.value()
            self.timerTrials.start(100-speed)
        except Exception as e:
            self.UNKNOWNERROR = "Changing Titration Speed and " + str(e)
            self.errorMessage()

    def Pause(self):
        try:
            if(self.loadStop.text() == "PAUSE"):
                self.timerTrials.stop()
                self.loadStop.setText("RESUME")

            else :
                self.timerTrials.start(100-self.volumeSpeed.value())
                self.loadStop.setText("PAUSE")
        except Exception as e:
            self.UNKNOWNERROR = "Starting/Pausing the titration and " + str(e)
            self.errorMessage()

    def LoadHypo(self):
        try:
            self.marker = 0
            self.movie.setValue(int(self.LOADMARK))
            #self.loadNAOH.setEnabled(False)
            if(self.resumeFlag):
                self.resumeFlag = False
        except Exception as e:
            self.UNKNOWNERROR = "Refilling Burette and " +str(e)
            self.errorMessage()

    def update2(self):
        try:
            
            if(self.FlaDrop.text() == "Flask"):
                return
            if(self.start):
                self.errorFlag = 2
                self.errorMessage()
            else:
                 
                if(self.FlaDrop.name() == " NaOH "):
                    self.errorFlag = 10
                    self.errorMessage()
                
                elif(self.FlaDrop.name() == " Phenolphthalein "):
                    self.loadKIFLAG = True
                        
                elif(self.FlaDrop.name() == " Acetic Acid " and self.LoadedINFLASK == False):
                    
                    self.FlaDrop.setImage("media/flask_ph.png")
                    self.phon=True
                    self.burVoldrop=0
                    #self.FlaDrop.setStyleSheet("QLineEdit {color: black; background-image : url(media/flask_ph.png); background-repeat: no-repeat;background-position: 0% 0%;}")
                    self.LoadedINFLASK = True
                    self.Calib_mode=False
                    self.volFlask = self.FlaDrop.vol()
                    self.conFlask = self.FlaDrop.con()
                    
                       
                    '''   
                    else :
                        self.errorFlag = 8
                        self.errorMessage()
                    '''
                
                elif(self.FlaDrop.name() == " Acidic Buffer " and self.LoadedINFLASK == False):
                    self.FlaDrop.setImage("media/flask_ph.png")
                    self.phon=True
                    #self.FlaDrop.setStyleSheet("QLineEdit {color: black; background-image : url(media/flask_ph.png); background-repeat: no-repeat;background-position: 0% 0%;}")
                    self.LoadedINFLASK = True
                    self.Calib_mode=True
                    self.conFlask = self.FlaDrop.con()

                    self.phDisplay.setText(str(self.conFlask))
                       
                    '''   
                    else :
                        self.errorFlag = 8
                        self.errorMessage()
                    '''
                    
                elif(self.FlaDrop.name() == " Oxalic Acid " and self.LoadedINFLASK==False):
                    self.FlaDrop.setImage("media/flask_ph.png")
                    self.phon=False
                    #self.FlaDrop.setStyleSheet("QLineEdit {color: black; background-image : url(media/flask_ph.png); background-repeat: no-repeat;background-position: 0% 0%;}")
                    self.LoadedINFLASK = True
                    
                    self.volFlask = self.FlaDrop.vol()*self.FlaDrop.con()
                    self.conFlask = self.volFlask
                       
                    '''   
                    else :
                        self.errorFlag = 8
                        self.errorMessage()
                    '''
                    
                else:
                    self.errorFlag = 11
                    self.errorMessage()   
            self.FlaDrop.setText("Flask")
            
        except Exception as e :
            self.UNKNOWNERROR = "Updating Flask parameters "+str(e)
            self.errorMessage()
            self.FlaDrop.setText("Flask")
           
            
        
    def START2(self):
        try:
            if(self.LoadedINFLASK and  self.burFlag):
                if(self.loadKIFLAG):
                    
                    self.volumeDown = (100*self.conFlask)/self.burCon
                    self.marker = 0
                    self.volumeDown = int(self.volumeDown)
                    #print(self.volumeDown)

                    self.start = True    
                    self.timerTrials.start(100-self.volumeSpeed.value())
                    self.loadStart.setEnabled(False)
                    self.loadStop.setEnabled(True)
                else:
                    self.errorFlag = -1
                    self.errorMessage()
            else :
                self.errorFlag = -2
                self.errorMessage()
        except:
            self.UNKNOWNERROR = "Starting the reaction"
            self.errorMessage()
    
    def cal_ph(self):
        oh_mm=self.burVoldrop*self.burCon/100
        hac_mm=self.conFlask*self.volFlask

        if (oh_mm<=hac_mm):
            self.phDisplay.setText(str(round(4.74+math.log10(oh_mm/(hac_mm-oh_mm))+self.extra,3)))
        else:
            if(self.value_vol):
                self.value_vol=False
                self.dataGEN[1]=self.burVoldrop/100
            
            if (oh_mm-hac_mm < 20):
                self.FlaDrop.setImage("media/flask_ph_change.png")
                
                #self.FlaDrop.setStyleSheet("QLineEdit {color: black; background-image : url(media/flask_ph_change.png); background-repeat: no-repeat;background-position: 0% 0%;}")

            elif(self.excess==False):
                self.FlaDrop.setImage("media/flask_ph_dark_change.png")
                self.excess = True

            self.phDisplay.setText(str(round(14-(-math.log10((oh_mm-hac_mm)/(self.burVoldrop/100+self.volFlask))+self.extra),3)))
        
        
    def hiddenTimer(self):
        try:
            if self.start and self.resumeFlag == False:
                
                self.volumeDown -= 1
                self.marker += 1
                self.burVoldrop +=1

            if(self.phon ==False): 
                
                if (self.volumeDown <= 20 and self.volumeDown >= -20):
                    self.FlaDrop.setImage("media/flask_ph_change.png")
                    #self.FlaDrop.setStyleSheet("QLineEdit {color: black; background-image : url(media/flask_ph_change.png); background-repeat: no-repeat;background-position: 0% 0%;}")

                elif(self.volumeDown <= -20 and self.volumeDown >= -25):
                    self.FlaDrop.setImage("media/flask_ph_dark_change.png")
                    #self.FlaDrop.setStyleSheet("QLineEdit {color: black; background-image : url(media/flask_ph_dark_change.png); background-repeat: no-repeat;background-position: 0% 0%;}")

            if self.start:
                #text = (self.volumeDown/100)
                self.movie.setValue(int(self.LOADMARK-self.marker))
                self.volumeDisplay.setText(str(round(self.marker/100, 1)))
                if(self.phon):
                    self.cal_ph()


                
                if(self.LOADMARK-self.marker <= -4999):
                    self.timerTrials.stop()
                    #self.RESETDROP(self.TitDrop, "Bur")
                    #print(self.volumeDown)
                    self.loadStop.setText("RESUME")
                    self.loadNAOH.setEnabled(True)
                    self.resumeFlag = True
                    self.errorFlag = 12
                    self.errorMessage()
                    
                
            
        except Exception as e:
            #print(e)
            self.UNKNOWNERROR = "Starting/Stoping Timer and " + str(e)
            self.errorMessage()

    def setUPtable(self):
        names = ["Sols->", " NaOH ", " Acetic Acid ", " Acidic Buffer ", " Oxalic Acid ", " Phenolphthalein "]
        for i in range(6) :
            self.SolsTab.setCellWidget(0, i, ImageLabel(names[i]))

            if(i):
                self.SolsTab.setCellWidget(3, i, DragLabel(names[i], "media/light2.png", True, self))
                self.SolsTab.setCellWidget(4, i, QDoubleSpinBox())
                self.SolsTab.cellWidget(4, i).valueChanged.connect(self.VolEntry)
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
        self.conc_na= 1+(random.randint(-25, 25)/100)     
        self.SolsTab.cellWidget(3, 1).setCon(self.conc_na)

        self.SolsTab.cellWidget(1, 1).setText("~1 N")
        self.SolsTab.cellWidget(3, 1).setCol(1)
        self.SolsTab.cellWidget(2, 1).setValue(50)
        
        
        
        

        temp=round(0.2+(random.randint(0, 20)/100),2)
        self.SolsTab.cellWidget(3, 2).setCon(temp)
        self.SolsTab.cellWidget(1, 2).setText(str(temp))
        self.SolsTab.cellWidget(2, 2).setValue(50)
        self.SolsTab.cellWidget(3, 2).setCol(2)
        
        buff = 4+(random.randint(-99, 99)/100)
        self.SolsTab.cellWidget(3, 3).setCon(buff)
        self.extra = buff-4
        self.SolsTab.cellWidget(1, 3).setText("pH 4")
        self.SolsTab.cellWidget(2, 3).setValue(15)


        self.SolsTab.cellWidget(3, 4).setCon(0.3)
        self.SolsTab.cellWidget(1, 4).setText("0.3N")
        self.SolsTab.cellWidget(2, 4).setValue(30)
        self.SolsTab.cellWidget(3, 4).setCol(2)

        self.SolsTab.cellWidget(3, 5).setCon(4.1)
        self.SolsTab.cellWidget(3, 5).setCol(0)
        self.SolsTab.cellWidget(1, 5).setText("~4.1M")
        self.SolsTab.cellWidget(2, 5).setValue(4)
        
        self.SolsTab.resizing()

        self.SolsTab.cellWidget(3, 5).setImage("media/pink2.png")

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

    def setUPTITBOX(self):
        
        self.ButtonBox = VoHGroup("V")
        self.ButtonBox.addWidgets([self.loadNAOH, self.loadStart, self.loadStop, self.loadRe])

        self.SPEEDLAB = ImageLabel("-SPEED-")
        self.SPEEDLay = QVBoxLayout()
        self.SPEEDBOX = VoHGroup("V")
        self.SPEEDBOX.addWidgets([self.volumeSpeed,self.SPEEDLAB])
            
        self.MISCBOX = VoHGroup("V")
        self.MISCBOX.addWidgets([self.volumeDisplay, self.ButtonBox, self.SPEEDBOX])
    
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