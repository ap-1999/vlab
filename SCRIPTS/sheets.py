import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.http import MediaFileUpload
from datetime import datetime
import os.path
from io import BytesIO
import sys
from base64 import urlsafe_b64encode
from email.mime.text import MIMEText
from PyQt5.QtWidgets import QMessageBox

credentials = {
  "type": "service_account",
  "project_id": "vlab-manage",
  "private_key_id": "75ec665edcdd624fc6b4ff1d8940920cbb91e0bc",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCviGF7Ho88YgeD\nZ3XOQR5nDGvIJpnrBYQJYeH0kE7cIpdG6TypivvLCXBNEpY6oQEdc6tCAjedtrnT\nuyqejHWsUlysOrjHWbHAZOArTcgWL6mwZL1DSZFOpIldT/vnkRlbxQTuhWixsDEs\nTYixikXOmr6UAkvFcDN6HPMUxY3XmR1XXhcgJLPqxmatB+7hxeP63b/FuBDjxq5n\nEduBfWUOztUaUBcjIv+halIAf/PCi6Xlijp4K/eBixlyaKV8lhNt5hvDIRZAUYz+\n3vpvidzEkSYF/AbpLuIJqHuAQgplxBaXDogH1rgc56g2S6idtukTUUeLFEAKeaAj\n7VPoMlc7AgMBAAECggEAGV14K1tyJVlLw/r/tLYHl6qIKgccoi/3htzkfaZwztzC\nHCwjaPiS2XcxXuHQYFktw7zC7an2XCMF3V55kn8HmMbaFMVI4v3Hct7g30EWfdDr\nZiMDOnr3YB7kqV2f2t7xLtKx8L8fLuDKv5/V9e8zlonD/7gJN6xhXpmvrWZoJdRW\njsBPDhUCxp41zTQ5cHrvRPsOdB5EgOCtB9RfJOLnypZPfO6HQ0kNiPMXUgRLMpCo\n0n0ALQOHj3mu+DyhvX/3Hpdg0lhSkUtV+d7/FYGMJxRHv+tXE414153mre6CgLmV\nnPnJlyt6RJk0QSrODEwuEwZefCjueYlNdimrbDAvwQKBgQDoW8gaL3/DimSCradj\nNGZBvZsxUTfE4ti+kR34EhiYVAMNHHae3CqDT7lm/vrGtPyo3edB1SdplQCOrpFY\nPH07vByF/oGd2C9aVzj0MdMYiWo1NqcMdB1XA5yPanYNljb7D7ZW/+1L6FC372Vo\nwawaE/5+/pjHTPO862Awf6YQYQKBgQDBZHa8S+SOv2rhf9vGby5stasz6XK8tpZS\nAGQGpovXox9X65f1IhBQgnCDENlBzuTLegD846+PWPfUGrkSY73tS7zul8zi11zr\n7yOrWLzXAp3wb2AtuwDBMWKtXe43T2i/6W6YNl5b/km7E87HsQT8mC0WWZaV2+K9\n54rjSve9GwKBgCM3jfuSCW5MsnEv+rfJgFokb7oo0igQLcOsYPtxWrLzwMai8sOf\nIP5n/fTDXqTxV34Mq/lJYkDZaY02nibefCiqmTQh3+lZk8vAfoxcZN9KLIPGNclo\na+39SSRfgWcLxmeE+SD0hzXDD0DhkuAuwnPtZdw/oE5MtoCCuECBiFzhAoGAUkAJ\nI8JfXbrZmTiI31dv9jo5qyVxcANz4UJbSFzTAw5UiU8g3Nf0+ljPw16KGCwHMOcd\nvnCTvTLIjIQlDEYxg9f/bbZQJHYWBh46HGjsP8HULGsiC7EJ/CCl6DgX1ZxHX7/H\nEqOk9BktgIxHGLUX+to56tSFcA0J3Vy5vDupK9sCgYEAxq3FWnh0ZJeVZAjKdr0G\nQkQ8pgpZv6gq4JFtF0SAIW3cfUUgr7iqxnbmhVoZGeJXIobVwNc78gV5nKTyxT4I\nX8eejVXFPmdzQDiwjUua/C0wJbiYtuoz0lWuI31+zxHWktcg7PqYlz2bF7mOTPNY\n18mRg3Pw91kK0myhT8oXHpk=\n-----END PRIVATE KEY-----\n",
  "client_email": "vlab-bot@vlab-manage.iam.gserviceaccount.com",
  "client_id": "110565675141477395639",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/vlab-bot%40vlab-manage.iam.gserviceaccount.com"
}

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', 
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive",
         ] 

creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials,scope)
client = gspread.authorize(creds)

sheet = []

Folder_ID = []
        
def Initialize() :
        try:
                global sheet
                sheet = client.open("Creds_Vlab").sheet1
                global Folder_ID
                Folder_ID = [sheet.cell(2,1).value, sheet.cell(2,2).value, sheet.cell(2,3).value, sheet.cell(2,4).value, sheet.cell(2,5).value, sheet.cell(2,6).value, sheet.cell(2,7).value]
                return 1
                
        except Exception as e:
                errorMessage()
                return 0

def loginverify(username,password):
        try:
                userid=[]
                usernameslist = sheet.col_values(2)
                usernameslist = usernameslist[4:]
                k=1
                for i in usernameslist  :
                        k=k+1
                        if username == i: 
                                userid = [sheet.cell(k+4, 2).value, sheet.cell(k+4, 3).value]
                                if userid[1] == password :
                                        return (1, getDetails(username, k+4), k+1)
                                break

                return (0, 0, 0)
        except Exception as e:
                #print(e)
                errorMessage()
                return (0,0,0)

def UploadImage(DATA_Misc, location, k, exp, whichCol):
        try:
                if(Folder_ID[exp] == "" or Folder_ID[exp] == None):
                    exp = 0
                service = build('drive', 'v3', credentials=creds, static_discovery=False)     
                file_metadata = {
                'name': str(str(DATA_Misc[0])+"_"+str(DATA_Misc[1])+".pdf"),
                'parents' : [Folder_ID[exp]]
                }
                
                media = MediaFileUpload(str(location),
                                        mimetype='application/pdf',
                                        )

                file = service.files().create(body=file_metadata,
                                                media_body=media,
                                                fields='id').execute()
                EXP = client.open("ReportFileList")
                temp = EXP.get_worksheet(exp-1)
                temp.update_cell(k, whichCol, file.get('id'))
                
                return file.get('id')
        except Exception as e:
                #print(e)
                errorMessage()
                return 0
                        
def getDetails(username, k):
        try:
                if(sheet.cell(k, 2).value == username):
                        userid = sheet.row_values(k)
                        return userid
                return None
        except:
                errorMessage()
                return None

def fetchDetails(username):
        try:
                usernameslist = sheet.col_values(2)
        
                k=0
                for i in usernameslist  :
                        k=k+1
                        if username == i:
                                userid = [sheet.cell(k, 2).value, sheet.cell(k, 3).value, sheet.cell(k, 4).value]
                                return userid
                return None
        except:
                errorMessage()
                return None

def getValidity():
        try:
                num = float(sheet.cell(3, 2).value)
                #print(num)
                if(num == 1):
                        return True
                return False
        except:
                return False
                                     
def UPLOADONDRIVE2(DATA_Misc, dataGEN, dataIN, labels, folder_id= 0 ):
        try:
                if(Folder_ID[folder_id] == "" or Folder_ID[folder_id] == None):
                    folder_id = 0
                service = build('drive', 'v3', credentials=creds, static_discovery=False)        
                
                stringdata = str(DATA_Misc[0])+"\n"+str(DATA_Misc[2])+"\n"+str(DATA_Misc[1])

                stringdata = stringdata + "\n\n-----:GENERATED:-----\n"

                flag = 0
                for i in dataGEN:
                        stringdata = stringdata+str(labels[flag])+" : "+str(i)+"\n"
                        flag+=1
                flag = 0
                stringdata = stringdata + "\n\n-----:USER INPUT:-----\n"
                for i in dataIN:
                        stringdata = stringdata+str(labels[flag])+" : "+str(i)+"\n"
                        flag+=1
                stringdata += "\nSTATUS : UNEVALUATED\nMARKS : 0"
                bio = BytesIO(stringdata.encode())
                file_meta = {"name": str(str(DATA_Misc[0])+"_"+str(DATA_Misc[1])+".txt"),
                             "parents": [Folder_ID[folder_id]]}
                
                media = MediaIoBaseUpload(bio, mimetype='text/plain',
                                          resumable=True)
                request = service.files().create(body=file_meta, media_body=media,
                                                 fields = 'id').execute()
                if request.get('id' )== None:
                        return 0
                exp = DATA_Misc[3]
                EXP = client.open("ReportFileList")
                temp = EXP.get_worksheet(exp-1)
                temp.update_cell(DATA_Misc[4], 3, request.get('id'))
                return 1
        except Exception as e:
                print(e)
                errorMessage()
                return 0

def errorMessage():
        w = QMessageBox()
        w.setText("Unable to connect")
        w.setInformativeText("Please check your internet connection. Or report a bug.")
        w.setWindowTitle("Error")
        w.exec() 
