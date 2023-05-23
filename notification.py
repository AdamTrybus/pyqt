from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from datetime import datetime
from datetime import date
from mesage import Message


class Notification(QWidget):
    signNotifyClose = pyqtSignal(str)

    def __init__(self, parent=None):
        time = datetime.now()
        currentTime = str(time.hour) + ":" + str(time.minute) + "_"
        self.LOG_TAG = currentTime + self.__class__.__name__ + ": "
        super(QWidget, self).__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        resolution = QDesktopWidget().screenGeometry(-1)
        screenWidth = resolution.width()
        screenHeight = resolution.height()
        print(self.LOG_TAG + "width: " + str(resolution.width()) +
              " height: " + str(resolution.height()))
        self.nMessages = 0
        self.mainLayout = QVBoxLayout(self)
        self.move(screenWidth, 0)

    def setNotify(self, title, message):
        m = Message(title, message, self)
        self.mainLayout.addWidget(m)
        m.buttonClose.clicked.connect(self.onClicked)
        self.nMessages += 1
        self.show()

    def onClicked(self):
        self.mainLayout.removeWidget(self.sender().parent())
        self.sender().parent().deleteLater()
        self.nMessages -= 1
        self.adjustSize()
        if self.nMessages == 0:
            self.close()
