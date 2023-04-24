from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import json


class DashboardWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Tworzenie listy wydarzeń
        self.event_table = QTableWidget(self)

        # Tworzenie listy dzisiejszych wydarzeń
        self.special_event_table = QTableWidget(self)
        self.special_event_table.setColumnCount(3)
        self.special_event_table.setHorizontalHeaderLabels(
            ['Święta', 'Imieniny', 'Urodziny'])
        self.event_table.setColumnCount(4)
        self.event_table.setHorizontalHeaderLabels(
            ['Godzina', 'Tytuł', 'Opis'])

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

    def set_events(self, events, date):
        self.date = date
        self.events = events
        self.event_table.setRowCount(len(events))
        for row, event in enumerate(events):
            time_item = QTableWidgetItem(event['time'])
            title_item = QTableWidgetItem(event['title'])
            description_item = QTableWidgetItem(event['description'])
            edit_button = QPushButton('Edytuj', self.event_table)
            edit_button.setFixedSize(50, 30)
            edit_button.clicked.connect(lambda: self.edit_event_dialog(event))
            self.event_table.setItem(row, 0, time_item)
            self.event_table.setItem(row, 1, title_item)

            self.event_table.setItem(row, 2, description_item)
            # Dodanie przycisku do wiersza
            self.event_table.setCellWidget(row, 3, edit_button)

    def set_special_events(self, events):
        self.events = events
        self.special_event_table.setRowCount(len(events))
        print(events)
        for row, event in enumerate(events):
            title_item = QTableWidgetItem(event['title'])
            if (event['genre'] == "b"):
                self.special_event_table.setItem(row, 2, title_item)
            elif (event['genre'] == "n"):
                self.special_event_table.setItem(row, 1, title_item)
            else:
                self.special_event_table.setItem(row, 0, title_item)
            # Dodanie przycisku do wiersza

    def edit_event_dialog(self, event):
        print(event)

        # Tworzenie okna dialogowego
        dialog = QDialog(self)
        dialog.setWindowTitle("Edytuj wydarzenie")
        dialog.resize(300, 200)

        # Tworzenie elementów formularza
        title_label = QLabel("Tytuł:", dialog)
        title_edit = QLineEdit(event['title'], dialog)
        description_label = QLabel("Opis:", dialog)
        description_edit = QLineEdit(event['description'], dialog)
        date_label = QLabel("Data:", dialog)

        date_edit = QDateEdit(QDate.fromString(
            event['date'], "yyyy-MM-dd"), dialog)
        time_label = QLabel("Godzina:", dialog)
        time_edit = QTimeEdit(QTime.fromString(event['time'], 'hh:mm'), dialog)

        # Tworzenie układu pionowego i dodanie do niego elementów formularza
        layout = QVBoxLayout(dialog)
        layout.addWidget(title_label)
        layout.addWidget(title_edit)
        layout.addWidget(description_label)
        layout.addWidget(description_edit)
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

    def add_event(self):
        # Tworzenie okna dialogowego
        dialog = QDialog(self)
        dialog.setWindowTitle("Dodaj wydarzenie")
        dialog.resize(300, 200)

        # Tworzenie elementów formularza
        title_label = QLabel("Tytuł:", dialog)
        title_edit = QLineEdit(dialog)
        description_label = QLabel("Opis:", dialog)
        description_edit = QLineEdit(dialog)
        date_label = QLabel("Data:", dialog)
        date_edit = QDateEdit(dialog)
        time_label = QLabel("Godzina:", dialog)
        time_edit = QTimeEdit(QTime.currentTime(), dialog)
        genre_label = QLabel("Typ:", dialog)
        genre_edit = QLineEdit(dialog)

        # Tworzenie układu pionowego i dodanie do niego elementów formularza
        layout = QVBoxLayout(dialog)
        layout.addWidget(title_label)
        layout.addWidget(title_edit)
        layout.addWidget(description_label)
        layout.addWidget(description_edit)
        layout.addWidget(date_label)
        layout.addWidget(date_edit)
        layout.addWidget(time_label)
        layout.addWidget(time_edit)
        layout.addWidget(genre_label)
        layout.addWidget(genre_edit)

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
        ), description_edit.text(), date_edit.date().toString("yyyy-MM-dd"), time_edit.time().toString("hh:mm")))

        cancel_button.clicked.connect(dialog.reject)

        # Wyświetlenie okna dialogowego
        dialog.exec_()

    def handle_save_button_click(self, dialog, event, title, description, date, time):
        self.delete_event(event)
        self.insert_event(title, description, date, time)

        # Zamknięcie okna dialogowego
        dialog.close()

        # Wczytanie wydarzeń z pliku JSON i zaktualizowanie kalendarza
        self.parent().parent().load_events_from_file('events.json')
        self.parent().parent().unhighlight_deleted_date(event)
        self.parent().parent().highlight_dates_with_events()
        self.parent().parent().update_events(self.date)

    def handle_delete_button_click(self, dialog, event):
        self.delete_event(event)

        # Zamknięcie okna dialogowego
        dialog.close()

        # Wczytanie wydarzeń z pliku JSON i zaktualizowanie kalendarza
        self.parent().parent().load_events_from_file('events.json')
        self.parent().parent().unhighlight_deleted_date(event)
        self.parent().parent().update_events(self.date)

    def handle_add_button_click(self, dialog, title, description, date, time):
        self.insert_event(title, description, date, time)

        # Zamknięcie okna dialogowego
        dialog.close()

        # Wczytanie wydarzeń z pliku JSON i zaktualizowanie kalendarza
        self.parent().parent().load_events_from_file('events.json')
        self.parent().parent().highlight_dates_with_events()

        self.parent().parent().update_events(self.date)

    def insert_event(self, title, description, date, time):
        # Wczytanie istniejących wydarzeń z pliku JSON
        with open('events.json', 'r') as f:
            events_json = json.load(f)

        # Dodanie nowego wydarzenia do listy
        new_event = {'title': title, 'description': description,
                     'date': date, 'time': time, }
        events_json.append(new_event)

        # Zapisanie zmienionej listy do pliku JSON
        with open('events.json', 'w') as f:
            json.dump(events_json, f)

    def delete_event(self, event):
        # Usunięcie wydarzenia z pliku JSON
        with open('events.json', 'r') as f:
            events_json = json.load(f)

        events_json.remove(event)

        with open('events.json', 'w') as f:
            json.dump(events_json, f)
