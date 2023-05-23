from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton
from PyQt5.QtGui import QIcon


class Message(QWidget):
    def __init__(self, title, message, parent=None):
        QWidget.__init__(self, parent)
        self.setLayout(QGridLayout())
        self.titleLabel = QLabel(title, self)
        self.titleLabel.setStyleSheet(
            "font-family: 'Roboto', sans-serif; font-size: 14px; font-weight: bold; padding: 0;")
        self.messageLabel = QLabel(message, self)
        self.messageLabel.setStyleSheet(
            "font-family: 'Roboto', sans-serif; font-size: 12px; font-weight: normal; padding: 0;")
        self.buttonClose = QPushButton(self)
        self.buttonClose.setIcon(QIcon("res/close1.png"))
        self.buttonClose.setFixedSize(14, 14)
        self.layout().addWidget(self.titleLabel, 0, 0)
        self.layout().addWidget(self.messageLabel, 1, 0)
        self.layout().addWidget(self.buttonClose, 0, 1, 2, 1)
