from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class SettingsManager(QObject):
    __instance = None
    background_color_changed = pyqtSignal(QColor)

    def __init__(self):
        super().__init__() # call the __init__() method of the super-class
        if SettingsManager.__instance is not None:
            raise Exception("Singleton class, use instance() method to get object")
        self.background_color = QColor(Qt.white)

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def set_background_color(self, color):
        if color is not None:
            self.background_color = color
            self.background_color_changed.emit(color)

    def get_background_color(self):
        return self.background_color
