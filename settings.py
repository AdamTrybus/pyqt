from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from settings_manager import SettingsManager

class Settings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.layout = QVBoxLayout()
        
        self.color_label = QLabel("Wybierz kolor tła kalendarza:")
        self.color_combo_box = QComboBox()
        self.color_combo_box.addItem("Biały")
        self.color_combo_box.addItem("Niebieski")
        self.color_combo_box.addItem("Zielony")
        self.color_combo_box.addItem("Czerwony")
        self.color_combo_box.addItem("Żółty")
        self.color_combo_box.addItem("Różowy")
        self.color_combo_box.addItem("Fioletowy")
        
        self.layout.addWidget(self.color_label)
        self.layout.addWidget(self.color_combo_box)
        
        self.setLayout(self.layout)

    def get_selected_color(self):
        color_name = self.color_combo_box.currentText()
        if color_name == "Biały":
            return Qt.white
        elif color_name == "Niebieski":
            return Qt.blue
        elif color_name == "Zielony":
            return Qt.green
        elif color_name == "Czerwony":
            return Qt.red
        elif color_name == "Żółty":
            return Qt.yellow
        elif color_name == "Różowy":
            return Qt.magenta
        elif color_name == "Fioletowy":
            return Qt.darkMagenta

    def closeEvent(self, event):
        settings_manager = SettingsManager.instance()
        color = self.get_selected_color()
        settings_manager.set_background_color(color)
        event.accept()
