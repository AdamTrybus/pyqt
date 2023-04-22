from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class DashboardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Tworzenie listy wydarzeń
        self.event_table = QTableWidget(self)
        self.event_table.setColumnCount(2)
        self.event_table.setHorizontalHeaderLabels(['Godzina', 'Opis'])

        # Tworzenie przycisków
        self.button1 = QPushButton("Przycisk 1", self)
        self.button2 = QPushButton("Przycisk 2", self)

        # Tworzenie układu horyzontalnego i dodanie do niego przycisków
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)

        # Tworzenie układu pionowego i dodanie do niego listy wydarzeń i układu przycisków
        layout = QVBoxLayout(self)
        layout.addWidget(self.event_table)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def set_events(self, events):
        self.event_table.setRowCount(len(events))
        for row, event in enumerate(events):
            time_item = QTableWidgetItem(event['time'])
            title_item = QTableWidgetItem(event['title'])
            self.event_table.setItem(row, 0, time_item)
            self.event_table.setItem(row, 1, title_item)

