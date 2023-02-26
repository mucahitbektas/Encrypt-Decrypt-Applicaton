from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication
from datetime import datetime
import locale
import os
import logging
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
import pathlib
import shutil


ALLOWED_FILES = [".txt",".png",".jpg",".jpeg",".gif",".doc","docx",".mp4",".mp3",".pdf",".odt",".xls",".xlsx",".json",".php",".exe",".sql",".csv",".xml",""]

class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(475, 360)
        Form.setMaximumSize(475, 360)
        Form.setMinimumSize(475, 360)

        Form.setWindowIcon(QtGui.QIcon("icons/icon.ico"))
        self.firstPixLabel = 10
        self.secondPixLabel = 270
        self.thirdPixLabel = 110
        self.fourthPixLabel = 450
        self.recentMailsHidden = True
        self.isDarkModeOn = False
        self.timer = QtCore.QTimer()
        self.timer.start(10)
        self.mode="-empty-"
        self.filePath=""
        self.user=""
        self.password=""
        self.lenght=0
        self.cc=""
        self.morefilenumber=0

        self.sentOrErrorLabel = QtWidgets.QLabel("", Form)
        self.sentOrErrorLabel.setGeometry(QtCore.QRect(170, 330, 300, 20))  
        self.sentOrErrorLabel.setObjectName("sentOrErrorLabel")
        self.sentOrErrorLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.sentOrErrorLabel.setText("-")

        self.attachedOrErrorLabel = QtWidgets.QLabel("", Form)
        self.attachedOrErrorLabel.setGeometry(QtCore.QRect(self.firstPixLabel, 130, 455, 20))
        self.attachedOrErrorLabel.setObjectName("attachedOrErrorLabel")
        self.attachedOrErrorLabel.setText("ATTACHED FİLE: -")

        self.runtimeLabel = QtWidgets.QPlainTextEdit(Form)
        self.runtimeLabel.setGeometry(QtCore.QRect(self.firstPixLabel, 195, 455, 130))
        self.runtimeLabel.setReadOnly(True)

        self.processButton = QtWidgets.QPushButton(Form)
        self.processButton.setGeometry(QtCore.QRect(240, 10, 225, 50))
        self.processButton.setObjectName("ProcessButton")

        self.pathPushButton = QtWidgets.QPushButton(Form)
        self.pathPushButton.setGeometry(QtCore.QRect(self.firstPixLabel, 10, 225, 50))
        self.pathPushButton.setObjectName("PathPushButton")

        self.keyLineEdit = QtWidgets.QLineEdit(Form)
        self.keyLineEdit.setGeometry(QtCore.QRect(self.firstPixLabel, 160, 455, 25))
        self.keyLineEdit.setObjectName("keyLineEdit")
        self.keyLineEdit.setPlaceholderText("Key")
        self.keyLineEdit.setText(Fernet.generate_key().decode())

        self.dateAndTimeLabel = QtWidgets.QLabel(Form)
        self.dateAndTimeLabel.setGeometry(QtCore.QRect(self.firstPixLabel, 330, 200, 20))
        self.dateAndTimeLabel.setObjectName("dateAndTimeLabel")
        self.dateAndTimeLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.themeCheckBox = QtWidgets.QCheckBox(Form)
        self.themeCheckBox.setGeometry(QtCore.QRect(40, 85, 120, 20))
        self.themeCheckBox.setObjectName("themeCheckBox")

        self.comboxBox = QtWidgets.QComboBox(Form)
        self.comboxBox.setGeometry(QtCore.QRect(310, 82, 120, 25))
        self.comboxBox.setObjectName("comboxBox")
        self.comboxBox.addItem("-empty-")
        self.comboxBox.addItem("Encyrpt")
        self.comboxBox.addItem("Decyrpt")

        self.sendMailDialog = QtWidgets.QDialog(Form)
        self.sendMailDialog.resize(400, 800)
        self.sendMailDialog.setWindowTitle("Cyrpto Operation")
        self.sendMailDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        self.sendMailDialog.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.sendMailDialog.setMinimumSize(200,800)

        self.logTextBox = QTextEditLogger(self.sendMailDialog)
        self.logTextBox.setFormatter(logging.Formatter('%(levelname)s - %(message)s - %(asctime)s '))
        logging.getLogger().addHandler(self.logTextBox)
        logging.getLogger().setLevel(logging.NOTSET)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.logTextBox.widget)
        self.sendMailDialog.setLayout(layout)
        self.sendMailDialog.move(300, 100)

        self.comboxBox.activated[str].connect(self.onChanged)
        self.processButton.clicked.connect(self.CryptOperation)
        self.pathPushButton.clicked.connect(self.attachFile)
        self.themeCheckBox.stateChanged.connect(self.themeCheckBoxStateChanged)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        curLocale = locale.getlocale()
        locale.setlocale(locale.LC_TIME, curLocale)
        dateAndTime = datetime.now()
        currentDate = datetime.strftime(dateAndTime, "%D %X")

        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "| Crypto Operation"))
        self.processButton.setText(_translate("Form", "Process"))
        self.dateAndTimeLabel.setText(_translate("Form", "Date: " + currentDate))
        self.themeCheckBox.setText(_translate("Form", "Dark Mode"))
        self.pathPushButton.setText(_translate("Form", "Attach File"))

    def key_creator(self):
        self.emit("Encryption key caught on keyLineEdit")
        key = self.keyLineEdit.text()
        print("Encryption Key: " + str(key))
        return key
        
    def CryptOperation(self):
        name,extension = os.path.splitext(self.filePath)
        key = self.key_creator()
        extension = extension.lower()
        if extension in ALLOWED_FILES:
            if self.mode == "Encyrpt":
                self.encrypt(key)
            if self.mode == "Decyrpt":
                self.decrypt(key)

    def crypto_details(self, name, extension, key):
        splitted = name.split("\\")
        name = splitted[len(splitted)-1]
        dir_name = name + "cryptoDetails"
        path = pathlib.Path(self.filePath)
        os.chdir(path.parent)
        os.mkdir(dir_name)
        new_dir = os.path.join(path.parent,dir_name)
        os.chdir(new_dir)
        write = str(datetime.now()) + "," + extension + "," + str(key)  
        
        with open('crypto_details.txt', 'w', encoding="UTF-8") as file:
            file.write(write)

        return new_dir
    
    def encrypt(self, key):
        if(os.path.exists(self.filePath)):
            file = open(self.filePath,"rb+")
            data = file.read()
            file.seek(0)

            if(len(data) > 0):
                name,extension = os.path.splitext(self.filePath)
                new_dir = self.crypto_details(name, extension, self.keyLineEdit.text())
                new_name = name+"_rimenc"
                i = 0
                while os.path.exists(new_name) == True :
                    i += 1
                    new_name = name+"_"+str(i)+extension+"_rimenc"

                fernet = Fernet(key)
                try :
                    encrypted = fernet.encrypt(data)

                except TypeError:
                    print("FAILED '"+self.filePath+"' could not encrypted because the data is not binary")
                    file.close()
                else:
                    change = file.write(encrypted)
                    file.close()
                    os.rename(self.filePath,new_name)
                    shutil.move(new_name,new_dir)

                self.emit("SUCCESS '"+self.filePath +"' has encrypted and renamed as '"+new_name+"'")
            else :
                self.emit("WARNING '"+self.filePath +"' could not encrypted because it's empty")
                file.close()
        

    def decrypt(self, key):
        if(os.path.exists(self.filePath) == True):
            new_name = self.filePath.rstrip("_rimenc")
            os.rename(self.filePath,new_name)
            file = open(new_name,"rb+")
            data = file.read()
            file.close()

            if(len(data) > 0):
                fernet = Fernet(key)
                try :
                    decrypted = fernet.decrypt(data)
                except InvalidToken:
                    self.emit("FAILED '"+self.filePath +"' could not decrypted because key invalid")
                    os.rename(new_name,self.filePath)
                except TypeError:
                    self.emit("FAILED '"+self.filePath +"' could not decrypted because the data is not binary")
                    os.rename(new_name,self.filePath)
                else :
                    file = open(new_name,"wb")
                    change = file.write(decrypted)
                    file.close()
                    self.emit("SUCCESS '"+self.filePath +"' has decrypted and renamed as '"+new_name+"'")
            else :
                self.emit("WARNING '"+self.filePath +"' could not decrypted because it's empty")
            
    def setContent(self, content, level):
        QApplication.processEvents()
        if level == "info":
            logging.info(content)
        if level == "error":
            logging.error(content)

    def emit(self, record):
        self.runtimeLabel.appendPlainText(record)

    def themeCheckBoxStateChanged(self):
        lightTheme = (open("themes\\lightTheme.qss", "r").read())
        darkTheme = (open("themes\\darkTheme.qss", "r").read())
        if self.themeCheckBox.isChecked():
            app.setStyleSheet(darkTheme)
            self.isDarkModeOn = True
        else:
            app.setStyleSheet(lightTheme)
            self.isDarkModeOn = False

    def attachFile(self):
        if self.mode != "-empty-":
            filePath , check = QFileDialog.getOpenFileName(None, 'Open file','C:\\',"All files (*.*)")
            try:
                if check:
                    with open(f'{filePath}', encoding="utf8"):
                        self.filePath = filePath
                        self.attachedOrErrorLabel.setText("ATTACHED FİLE: {}".format(filePath))
                        # webbrowser.open(filePath)
            except Exception as e:
                print(e)

        else:
            self.emit("Please select mode.")

    def onChanged(self, text):
        self.mode = text
        self.emit("Set to {} Mode".format(text))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    app.setStyleSheet(open("themes\\lightTheme.qss", "r").read())
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
