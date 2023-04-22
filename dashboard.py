from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import json

class DashboardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Tworzenie listy wydarzeń
        self.event_table = QTableWidget(self)
        self.event_table.setColumnCount(2)
        self.event_table.setHorizontalHeaderLabels(['Godzina', 'Opis'])

        # Tworzenie przycisków
        self.button1 = QPushButton("Przycisk 1", self)
        self.button1.clicked.connect(self.add_event)
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

    def add_event(self):
        # Tworzenie okna dialogowego
        dialog = QDialog(self)
        dialog.setWindowTitle("Dodaj wydarzenie")
        dialog.resize(300, 200)

        # Tworzenie elementów formularza
        title_label = QLabel("Tytuł:", dialog)
        title_edit = QLineEdit(dialog)
        date_label = QLabel("Data:", dialog)
        date_edit = QDateEdit(QDate.currentDate(), dialog)
        time_label = QLabel("Godzina:", dialog)
        time_edit = QTimeEdit(QTime.currentTime(), dialog)

        # Tworzenie układu pionowego i dodanie do niego elementów formularza
        layout = QVBoxLayout(dialog)
        layout.addWidget(title_label)
        layout.addWidget(title_edit)
        layout.addWidget(date_label)
        layout.addWidget(date_edit)
        layout.addWidget(time_label)
        layout.addWidget(time_edit)

        # Tworzenie przycisków
        add_button = QPushButton("Dodaj", dialog)
        cancel_button = QPushButton("Anuluj", dialog)

        # Tworzenie układu horyzontalnego i dodanie do niego przycisków
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(cancel_button)

        # Dodanie układu przycisków do układu pionowego
        layout.addLayout(button_layout)

        # Przypisanie funkcji do przycisków
        add_button.clicked.connect(lambda: self.insert_event(title_edit.text(), date_edit.date().toString("yyyy-MM-dd"), time_edit.time().toString("hh:mm")))
        cancel_button.clicked.connect(dialog.reject)

        # Wyświetlenie okna dialogowego
        dialog.exec_()

    def insert_event(self, title, date, time):
        # Wczytanie istniejących wydarzeń z pliku JSON
        with open('events.json', 'r') as f:
            events_json = json.load(f)
        
        # Dodanie nowego wydarzenia do listy
        new_event = {'date': date, 'time': time, 'title': title}
        events_json.append(new_event)

        # Zapisanie zmienionej listy do pliku JSON
        with open('events.json', 'w') as f:
            json.dump(events_json, f)

        # Wczytanie wydarzeń z pliku JSON i zaktualizowanie kalendarza
        self.parent().parent().load_events_from_file('events.json')
        self.parent().parent().highlight_dates_with_events()

