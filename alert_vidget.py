from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication
from PyQt5.QtCore import QPropertyAnimation, QRect, QParallelAnimationGroup, pyqtProperty, Qt
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush
from notification import Notification
import sys


class Example(QWidget):
    counter = 0

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setLayout(QVBoxLayout())
        btn = QPushButton("Send Notify", self)
        self.layout().addWidget(btn)

        self.notification = Notification()
        btn.clicked.connect(self.notify)

    def notify(self):
        self.counter += 1
        self.notification.setNotify("Title{}".format(self.counter),
                                    "message{}".format(self.counter))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Example()
    w.show()
    sys.exit(app.exec_())
