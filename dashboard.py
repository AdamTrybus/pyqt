from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import json


class DashboardWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Tworzenie listy wydarzeń
        self.event_table = QTableWidget(self)
        self.event_table.setColumnCount(3)
        self.event_table.setHorizontalHeaderLabels(
            ['Godzina', 'Opis', 'Edycja'])

        # Tworzenie listy dzisiejszych wydarzeń
        self.special_event_table = QTableWidget(self)
        self.special_event_table.setColumnCount(3)
        self.special_event_table.setHorizontalHeaderLabels(
            ['Święta', 'Imieniny', 'Urodziny'])

        # Tworzenie przycisków
        self.button1 = QPushButton("Dodaj", self)
        self.button1.clicked.connect(self.add_event)
        self.button2 = QPushButton("Przycisk 2", self)

        # Tworzenie układu horyzontalnego i dodanie do niego przycisków
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)

        #

        # Tworzenie układu pionowego i dodanie do niego listy wydarzeń i układu przycisków
        layout = QVBoxLayout(self)
        layout.addWidget(self.event_table)
        layout.addWidget(self.special_event_table)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def set_events(self, events):
        self.events = events
        self.event_table.setRowCount(len(events))
        for row, event in enumerate(events):
            time_item = QTableWidgetItem(event['time'])
            title_item = QTableWidgetItem(event['title'])
            edit_button = QPushButton('Edytuj', self.event_table)
            edit_button.setFixedSize(50, 30)
            edit_button.clicked.connect(lambda: self.edit_event_dialog(event))
            self.event_table.setItem(row, 0, time_item)
            self.event_table.setItem(row, 1, title_item)
            # Dodanie przycisku do wiersza
            self.event_table.setCellWidget(row, 2, edit_button)

    def set_special_events(self, events):
        self.events = events
        self.event_table.setRowCount(len(events))
        for row, event in enumerate(events):
            title_item = QTableWidgetItem(event['title'])
            if (event['genre'] == "b"):
                self.event_table.setItem(row, 2, title_item)
            elif (event['genre'] == "n"):
                self.event_table.setItem(row, 1, title_item)
            else:
                self.event_table.setItem(row, 0, title_item)
            # Dodanie przycisku do wiersza

    def edit_event_dialog(self, event):
        print(event)

        # Tworzenie okna dialogowego
        dialog = QDialog(self)
        dialog.setWindowTitle("Edytuj wydarzenie")
        dialog.resize(300, 200)

        # Tworzenie elementów formularza i wypełnienie ich aktualnymi danymi wydarzenia
        title_label = QLabel("Tytuł:", dialog)
        title_edit = QLineEdit(event['title'], dialog)
        date_label = QLabel("Data:", dialog)
        date_edit = QDateEdit(QDate.fromString(
            event['date'], "yyyy-MM-dd"), dialog)
        time_label = QLabel("Godzina:", dialog)
        time_edit = QTimeEdit(QTime.fromString(event['time'], "hh:mm"), dialog)

        # Tworzenie układu pionowego i dodanie do niego elementów formularza
        layout = QVBoxLayout(dialog)
        layout.addWidget(title_label)
        layout.addWidget(title_edit)
        layout.addWidget(date_label)
        layout.addWidget(date_edit)
        layout.addWidget(time_label)
        layout.addWidget(time_edit)

        # Tworzenie przycisków
        save_button = QPushButton("Zatwierdź", dialog)
        delete_button = QPushButton("Usuń", dialog)

        # Tworzenie układu horyzontalnego i dodanie do niego przycisków
        button_layout = QHBoxLayout()
        button_layout.addWidget(save_button)
        button_layout.addWidget(delete_button)

        # Dodanie układu przycisków do układu pionowego
        layout.addLayout(button_layout)

        # Przypisanie funkcji do przycisków
        save_button.clicked.connect(lambda: self.handle_save_button_click(dialog, event, title_edit.text(
        ), date_edit.date().toString("yyyy-MM-dd"), time_edit.time().toString("hh:mm")))

        delete_button.clicked.connect(
            lambda: self.handle_delete_button_click(dialog, event))

        # Wyświetlenie okna dialogowego
        dialog.exec_()

    def handle_save_button_click(self, dialog, event, title, date, time):
        self.delete_event(event)
        self.insert_event(title, date, time)

        # Zamknięcie okna dialogowego
        dialog.close()

        # Wczytanie wydarzeń z pliku JSON i zaktualizowanie kalendarza
        self.parent().parent().load_events_from_file('events.json')
        self.parent().parent().unhighlight_deleted_date(event)
        self.parent().parent().highlight_dates_with_events()

    def handle_delete_button_click(self, dialog, event):
        self.delete_event(event)

        # Zamknięcie okna dialogowego
        dialog.close()

        # Wczytanie wydarzeń z pliku JSON i zaktualizowanie kalendarza
        self.parent().parent().load_events_from_file('events.json')
        self.parent().parent().unhighlight_deleted_date(event)

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
        add_button.clicked.connect(lambda: self.handle_add_button_click(dialog, title_edit.text(
        ), date_edit.date().toString("yyyy-MM-dd"), time_edit.time().toString("hh:mm")))
        cancel_button.clicked.connect(dialog.reject)

        # Wyświetlenie okna dialogowego
        dialog.exec_()

    def delete_event(self, event):
        # Usunięcie wydarzenia z pliku JSON
        with open('events.json', 'r') as f:
            events_json = json.load(f)

        events_json.remove(event)

        with open('events.json', 'w') as f:
            json.dump(events_json, f)

    def handle_add_button_click(self, dialog, title, date, time):
        self.insert_event(title, date, time)

        # Zamknięcie okna dialogowego
        dialog.close()

        # Wczytanie wydarzeń z pliku JSON i zaktualizowanie kalendarza
        self.parent().parent().load_events_from_file('events.json')
        self.parent().parent().highlight_dates_with_events()
