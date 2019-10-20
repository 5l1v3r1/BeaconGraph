from PyQt5.QtCore import (QEasingCurve, QPropertyAnimation,
                          QSequentialAnimationGroup, Qt, QThread, QUrl,
                          pyqtSignal)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (QApplication, QBoxLayout, QDialog, QFormLayout,
                             QGraphicsOpacityEffect, QLabel, QLineEdit,
                             QMessageBox, QPushButton)

from neoHandler import neoHandler

qss = ("""
        QDialog {
            color: white;
            background-color: rgb(5, 5, 36);
            padding: 20px 20px 20px 20px;
            font-size: 14px;
        }

        QLabel {
            color: white;
            background-color: rgb(5, 5, 36);
            padding: 10px 20px 20px 20px;
            font-size: 14px;
        }
        QLineEdit {
            background-color: rgb(5, 5, 36);
            font-size: 14px;
            color: white;
            border-radius: 0px;
            padding: 10px 10px 10px 20px;
        }
        QLineEdit:focus {
            border: 1px solid white;
            border-radius: 2px;
        }
        QPushButton {
            color: white;
            background-color: rgb(5, 5, 36);
        }
        QMessageBox {
            color: white;
            background-color: rgb(5, 5, 36);
            padding: 10px 20px 20px 20px;
            font-size: 14px;
        }
        QWebEngineView {
            color: white;
            background-color: rgb(5, 5, 36);
            padding: 10px 20px 20px 20px;
            font-size: 14px;
        }
        """)


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.LOGGEDIN = False
        self.setWindowIcon(QIcon("assets/logo.png"))
        self.setWindowTitle("BeaconGraph")
        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)

        self.logo = QPixmap('assets/logo300.png')
        self.picLabel = QLabel(self)
        self.picLabel.setPixmap(self.logo)
        self.picLabel.setAlignment(Qt.AlignCenter)

        self.uri = QLineEdit(self)
        self.uri.setText("bolt://localhost:7687")
        self.QUriLabel = QLabel("DB URI")

        self.username = QLineEdit(self)
        self.username.setPlaceholderText("Neo4j Username")
        self.QUserLabel = QLabel("USERNAME")

        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Neo4j Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.QPasswordLabel = QLabel("PASSWORD")

        self.btn_Submit = QPushButton("LOGIN")

        self.setStyleSheet(qss)
        self.resize(400, 500)

        logoLayout = QBoxLayout(QBoxLayout.TopToBottom)
        logoLayout.addWidget(self.picLabel)

        layout = QFormLayout()
        layout.addRow(self.QUriLabel, self.uri)
        layout.addRow(self.QUserLabel, self.username)
        layout.addRow(self.QPasswordLabel, self.password)
        layout.addRow(self.btn_Submit)

        logoLayout.addLayout(layout)
        self.setLayout(logoLayout)
        self.btn_Submit.clicked.connect(self.Submit_btn)

    def Submit_btn(self):
        URI = self.uri.text()
        USERNAME = self.username.text()
        PASSWORD = self.password.text()
        try:
            self.neo = neoHandler(URI, USERNAME, PASSWORD)
            self.LOGGEDIN = True
            self.close()
        except Exception as e:
            err = QMessageBox()
            err.setStyleSheet(qss)
            err.setText(str(e.__context__))
            err.show()


class BeaconView(QWebEngineView):
    def __init__(self, url, parent=None):
        super(BeaconView, self).__init__(parent)
        self.setWindowIcon(QIcon("assets/logo.png"))
        self.setWindowTitle("BeaconGraph")
        self.setMinimumSize(1440, 900)
        self.setStyleSheet(qss)
        self.load(QUrl(url))

    def showStatus(self, text):
        pass
        #self.statusWid = StatusNotification(text, self)


class StatusNotification(QLabel):
    def __init__(self, text, upper, parent=None):
        super(StatusNotification, self).__init__(parent)
        self.setText("test")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setStyleSheet("""
            color: white;
            background-color: rgb(5, 5, 36);
            padding: 2px;
            font-size: 14px;
        """)
        self.setGeometry((upper.width()-100)/2, 0, 100, 20)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        effect = QGraphicsOpacityEffect()
        effect.setOpacity(1)
        self.setGraphicsEffect(effect)

        self.animations = QSequentialAnimationGroup(self)
        self.animations.addPause(3000)
        opacAnimation = QPropertyAnimation(effect, b"opacity", self.animations)
        opacAnimation.setDuration(2000)
        opacAnimation.setStartValue(1.0)
        opacAnimation.setEndValue(0.0)
        opacAnimation.setEasingCurve(QEasingCurve.OutQuad)
        self.animations.addAnimation(opacAnimation)
        self.animations.start()
        self.show()
