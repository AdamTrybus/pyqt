from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class DashboardWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(['Godzina', 'Opis'])

    def set_events(self, events):
        self.setRowCount(len(events))
        for row, event in enumerate(events):
            time_item = QTableWidgetItem(event['time'])
            title_item = QTableWidgetItem(event['title'])
            self.setItem(row, 0, time_item)
            self.setItem(row, 1, title_item)
