from PyQt5.QtWidgets import QLabel, QTimeEdit, QSystemTrayIcon, QDateEdit, QComboBox, QVBoxLayout,  QWidget, QTableWidget, QPushButton, QDialog, QHBoxLayout, QVBoxLayout, QFileDialog, QTableWidgetItem, QLineEdit, QMenu, QAction
from PyQt5.QtCore import QDate, QTime
from PyQt5.QtGui import QIcon
import json
import holidays
from settings import Settings
from icalendar_parser import CalendarParser
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class DashboardWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Tworzenie listy wydarzeń
        self.event_table = QTableWidget(self)

        # Tworzenie listy dzisiejszych wydarzeń
        self.special_event_table = QTableWidget(self)
        self.special_event_table.setColumnCount(3)
        self.event_table.setColumnCount(5)
        self.special_event_table.setHorizontalHeaderLabels(
            ['Święta', 'Imieniny', 'Urodziny'])
        self.event_table.setHorizontalHeaderLabels(
            ['Godzina', 'Tytuł', 'Opis', 'Edycja', 'Export'])

        # Tworzenie przycisków
        self.button1 = QPushButton("Dodaj", self)
        self.button1.clicked.connect(self.add_event)
        self.button2 = QPushButton("Ustawienia", self)
        self.button2.clicked.connect(self.open_settings_window)

        # Tworzenie układu horyzontalnego i dodanie do niego przycisków
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)

        # Tworzenie widgetów na dodatkowe informacje o dniu dzisiejszym i wybranym
        self.additional_info_table = QTableWidget(self)
        self.additional_info_table.setColumnCount(5)
        self.additional_info_table.setHorizontalHeaderLabels(
            ['Data', 'Dzień tygodnia', 'Dzień w roku', 'Tydzień w roku', 'Święto'])

        # Tworzenie layoutu horyzontalnego i dodanie do niego eventów
        side_layout = QVBoxLayout()
        side_layout.addWidget(self.special_event_table)
        side_layout.addWidget(self.additional_info_table)
        event_layout = QHBoxLayout()
        event_layout.addWidget(self.event_table)
        event_layout.addLayout(side_layout)

        # Tworzenie układu pionowego i dodanie do niego list wydarzeń i układu przycisków
        layout = QVBoxLayout(self)
        layout.addLayout(event_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def save_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            self, "QFileDialog.getSaveFileName()", "", "Calendar Files (*.ics)", options=options)
        if fileName:
            return fileName

    def open_file_name_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "", "Calendar Files (*.ics)", options=options)
        if fileName:
            print(fileName)
            return fileName

    def open_settings_window(self):
        self.new_window = Settings()
        self.new_window.show()
        self.trayIcon = QSystemTrayIcon()
        self.trayIcon.setIcon(QIcon())
        self.trayMenu = QMenu(self)
        self.trayIcon.setContextMenu(self.trayMenu)

        # Create an action to show the app window when the system tray icon is clicked
        showAction = QAction("Show", self)
        showAction.triggered.connect(self.show)

        # Add the action to the menu
        self.trayMenu.addAction(showAction)
        self.show()

    def checkEvents(self):
        message = "You have event(s) today!"
        self.trayIcon.showMessage(
            "Event Notification", message, QSystemTrayIcon.Information, 5000)

    def save_file(self, filename, event):
        if filename:
            self.choose_events_to_icalendar([event], filename=filename)

    # def handle_import_button_click(self, filename):
    #     if filename:
    #         self.load_from_icalendar(filename=filename)

    def set_events(self, events, date):
        self.date = date
        self.events = events
        self.event_table.setRowCount(len(events))
        print(events)
        for row, event in enumerate(events):
            time_item = QTableWidgetItem(event['time'])
            title_item = QTableWidgetItem(event['title'])
            description_item = QTableWidgetItem(event['description'])
            edit_button = QPushButton('Edytuj', self.event_table)
            edit_button.setFixedSize(50, 30)
            edit_button.clicked.connect(lambda: self.edit_event_dialog(event))
            export_button = QPushButton('Export', self.event_table)
            export_button.setFixedSize(50, 30)
            export_button.clicked.connect(
                lambda: self.save_file(self.save_file_dialog(), event))
            self.event_table.setItem(row, 0, time_item)
            self.event_table.setItem(row, 1, title_item)

            self.event_table.setItem(row, 2, description_item)
            # Dodanie przycisku do wiersza
            self.event_table.setCellWidget(row, 3, edit_button)
            self.event_table.setCellWidget(row, 4, export_button)

    def change_number_to_weekday_name(self, day_number):
        return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][day_number]

    # Dodawanie dodatkowych informacji o dniu

    def day_information(self, date):
        holidays_in_year = holidays.PL(2023)
        print(holidays_in_year.get(date.toPyDate()))
        if not holidays_in_year.get(date.toPyDate()):
            festival_item = QTableWidgetItem("")
        else:
            festival_item = QTableWidgetItem(
                holidays_in_year.get(date.toPyDate()))
        print("item", festival_item.text())
        day_of_week = QTableWidgetItem(
            self.change_number_to_weekday_name(date.toPyDate().weekday()))
        print(date.toPyDate().strftime("%j"))
        day_of_year = QTableWidgetItem(date.toPyDate().strftime("%j"))
        week_of_year = QTableWidgetItem(date.toPyDate().strftime("%W"))

        self.additional_info_table.setRowCount(1)
        self.additional_info_table.setItem(
            0, 0, QTableWidgetItem(date.toString()))
        self.additional_info_table.setItem(0, 1, day_of_week)
        self.additional_info_table.setItem(0, 2, day_of_year)
        self.additional_info_table.setItem(0, 3, week_of_year)
        self.additional_info_table.setItem(0, 4, festival_item)

    def set_special_events(self, events):
        # self.choose_events_to_icalendar(events)
        self.events = events
        self.special_event_table.setRowCount(len(events))
        print(events)
        row = 0
        for event in events:
            title_item = QTableWidgetItem(event['title'])
            if (event['genre'] == "b"):
                self.special_event_table.setItem(row, 2, title_item)
            elif (event['genre'] == "n"):
                self.special_event_table.setItem(row, 1, title_item)
            else:
                self.special_event_table.setItem(row, 0, title_item)
            row += 1
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

        genre_label = QLabel("Wybierz typ wydarzenia:", dialog)
        genres_combo_box = QComboBox(dialog)
        genres_combo_box.addItem("Kulturalne")
        genres_combo_box.addItem("Biznesowe")
        genres_combo_box.addItem("Święta")
        genres_combo_box.addItem("Naukowe")
        genres_combo_box.addItem("Urodziny")
        genres_combo_box.addItem("Imieniny")
        genres_combo_box.addItem("Inne")

        period_label = QLabel("Czy powtarzać:", dialog)
        period_combo_box = QComboBox(dialog)
        period_combo_box.addItem("Nigdy")
        period_combo_box.addItem("Cotygodniowo")
        period_combo_box.addItem("Dwutygodniowo")
        period_combo_box.addItem("Miesięcznie")
        if 'period' in event and event['period'] is None:
            period_combo_box.setCurrentText("Nigdy")
        elif 'period' in event:
            period_combo_box.setCurrentText(event['period'])

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
        layout.addWidget(genres_combo_box)
        layout.addWidget(period_label)
        layout.addWidget(period_combo_box)

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
        ), description_edit.text(), date_edit.date().toString("yyyy-MM-dd"), time_edit.time().toString("hh:mm"),
         genres_combo_box.currentText(), period_combo_box.currentText()))

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
        date_edit = QDateEdit(self.date, dialog)
        time_label = QLabel("Godzina:", dialog)
        time_edit = QTimeEdit(QTime.currentTime(), dialog)
        
        genre_label = QLabel("Wybierz typ wydarzenia:", dialog)
        genres_combo_box = QComboBox(dialog)
        genres_combo_box.addItem("Kulturalne")
        genres_combo_box.addItem("Biznesowe")
        genres_combo_box.addItem("Święta")
        genres_combo_box.addItem("Naukowe")
        genres_combo_box.addItem("Urodziny")
        genres_combo_box.addItem("Imieniny")
        genres_combo_box.addItem("Inne")

        period_label = QLabel("Czy powtarzać:", dialog)
        period_combo_box = QComboBox(dialog)
        period_combo_box.addItem("Nigdy")
        period_combo_box.addItem("Tygodniowo")
        period_combo_box.addItem("Dwutygodniowo")
        period_combo_box.addItem("Miesięcznie")


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
        layout.addWidget(genres_combo_box)
        layout.addWidget(period_label)
        layout.addWidget(period_combo_box)

        # Tworzenie przycisków
        add_button = QPushButton("Dodaj", dialog)
        cancel_button = QPushButton("Anuluj", dialog)
        import_button = QPushButton("Importuj", dialog)

        # Tworzenie układu horyzontalnego i dodanie do niego przycisków
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(import_button)

        # Dodanie układu przycisków do układu pionowego
        layout.addLayout(button_layout)

        # Przypisanie funkcji do przycisków
        add_button.clicked.connect(lambda: self.handle_add_button_click(dialog, title_edit.text(
        ), description_edit.text(), date_edit.date().toString("yyyy-MM-dd"), time_edit.time().toString("hh:mm"),
         genres_combo_box.currentText(), period_combo_box.currentText()))

        cancel_button.clicked.connect(dialog.reject)

        import_button.clicked.connect(
            lambda: self.handle_import_button_click(dialog, self.open_file_name_dialog()))

        # Wyświetlenie okna dialogowego
        dialog.exec_()

    def handle_save_button_click(self, dialog, event, title, description, date, time, genre, period):
        self.delete_event(event)
        self.insert_event(title, description, date, time, genre, period)

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

    def handle_add_button_click(self, dialog, title, description, date, time, genre, period):
        self.insert_event(title, description, date, time, genre, period)

        # Zamknięcie okna dialogowego
        dialog.close()

        # Wczytanie wydarzeń z pliku JSON i zaktualizowanie kalendarza
        self.parent().parent().load_events_from_file('events.json')
        self.parent().parent().highlight_dates_with_events()

        self.parent().parent().update_events(self.date)


    def insert_event(self, title, description, date, time, genre, period):
        # Wczytanie istniejących wydarzeń z pliku JSON
        with open('events.json', 'r') as f:
            events_json = json.load(f)

        # Dodanie nowego wydarzenia do listy
        new_event = {'title': title, 'description': description,
                    'date': date, 'time': time, 'genre': genre, 'period': period}
        events_json.append(new_event)

        # Generowanie dodatkowych wydarzeń w odpowiednich interwałach
        if period == "Cotygodniowo":
            current_date = datetime.strptime(date, "%Y-%m-%d")
            end_of_year = datetime(current_date.year, 12, 31)

            while current_date < end_of_year:
                current_date += timedelta(weeks=1)
                new_event = {'title': title, 'description': description,
                            'date': current_date.strftime("%Y-%m-%d"), 'time': time, 'genre': genre, 'period': period}
                events_json.append(new_event)

        elif period == "Dwutygodniowo":
            current_date = datetime.strptime(date, "%Y-%m-%d")
            end_of_year = datetime(current_date.year, 12, 31)

            while current_date < end_of_year:
                current_date += timedelta(weeks=2)
                new_event = {'title': title, 'description': description,
                            'date': current_date.strftime("%Y-%m-%d"), 'time': time, 'genre': genre, 'period': period}
                events_json.append(new_event)

        elif period == "Miesięcznie":
            current_date = datetime.strptime(date, "%Y-%m-%d")
            end_of_year = datetime(current_date.year, 12, 31)

            while current_date < end_of_year:
                current_date += relativedelta(months=1)
                new_event = {'title': title, 'description': description,
                            'date': current_date.strftime("%Y-%m-%d"), 'time': time, 'genre': genre, 'period': period}
                events_json.append(new_event)

        # Zapisanie zmienionej listy do pliku JSON
        with open('events.json', 'w') as f:
            json.dump(events_json, f)


    def delete_event(self, event):
        # Usunięcie wydarzenia z pliku JSON
        with open('events.json', 'r') as f:
            events_json = json.load(f)
            
        updated_events = [evt for evt in events_json if
                            (evt.get('title') != event.get('title') or
                            evt.get('description') != event.get('description') or
                            evt.get('time') != event.get('time') or
                            evt.get('genre') != event.get('genre') or
                            evt.get('period') != event.get('period'))]


        with open('events.json', 'w') as f:
            json.dump(updated_events, f)


    # Obliczanie dnia w roku
    # Parsowanie wydarzen do icalendar
    def choose_events_to_icalendar(self, events, filename):
        i_cal = CalendarParser(events, filename)
        i_cal.export_events_to_file()

    def handle_import_button_click(self, dialog, filename):
        i_cal = CalendarParser([], filename)
        events = i_cal.load_from_icalendar()
        print(events)
        for event in events:
            self.insert_event(event['title'], event['description'], event['date'],
                              event['time'], event['genre'], event['period'])
        dialog.close()

        # Wczytanie wydarzeń z pliku JSON i zaktualizowanie kalendarza
        self.parent().parent().load_events_from_file('events.json')
        self.parent().parent().highlight_dates_with_events()

        self.parent().parent().update_events(QDate.fromString(
            event['date'], "yyyy-MM-dd"))
