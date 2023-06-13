from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QColor


class SettingsManager(QObject):
    __instance = None
    background_color_changed = pyqtSignal(QColor)
    filters_changed = pyqtSignal(list)

    def __init__(self):
        super().__init__()  # call the __init__() method of the super-class
        if SettingsManager.__instance is not None:
            raise Exception(
                "Singleton class, use instance() method to get object")
        self.background_color = QColor(Qt.white)
        self.filters = ['Urodziny', 'Imieniny', 'Święta',
                        'Kulturalne', 'Biznesowe', 'Naukowe', 'Inne']

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

    def set_filters(self, filters):
        self.filters = filters
        self.filters_changed.emit(filters)

    def get_filters(self):
        return self.filters
