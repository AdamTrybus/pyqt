from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import json


class CalendarWidget(QWidget):
    def __init__(self, dashboard, parent=None):
        super().__init__(parent)

        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.clicked[QDate].connect(self.update_events)

        self.dashboard = dashboard

        self.splitter = QSplitter(self)
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.addWidget(self.calendar)
        self.splitter.addWidget(self.dashboard)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.splitter)
        self.setLayout(self.layout)

        self.events = self.load_events_from_file('events.json')
        self.highlight_dates_with_events()

    def load_events_from_file(self, filename):
        with open(filename, 'r') as f:
            events_json = json.load(f)
        self.events = events_json
        return self.events

    def update_events(self, date):
        # Tutaj powinna być logika filtrowania wydarzeń z listy self.events
        filtered_events = [
            event for event in self.events if event['date'] == date.toString(Qt.ISODate)]
        self.dashboard.set_events(filtered_events)

    def update_special_events(self, date):
        # filtrowanie urodzin, imienin, świąt
        today_events = [
            special_event for special_event in self.events if special_event['date'] == date.toString(Qt.ISODate)]
        self.dashboard.set_events(today_events)

    def highlight_dates_with_events(self):
        # Tworzenie formatu dla dat z wydarzeniami
        date_format = QTextCharFormat()
        date_format.setBackground(Qt.green)

        # Dodawanie formatu dla dat z wydarzeniami
        for event in self.events:
            event_date = QDate.fromString(event['date'], Qt.ISODate)
            self.calendar.setDateTextFormat(event_date, date_format)

    def unhighlight_deleted_date(self, event):
        # Tworzenie formatu dla usuniętej daty
        date_format = QTextCharFormat()
        date_format.setBackground(Qt.white)

        # Dodawanie formatu dla usuniętej daty
        event_date = QDate.fromString(event['date'], Qt.ISODate)
        self.calendar.setDateTextFormat(event_date, date_format)
