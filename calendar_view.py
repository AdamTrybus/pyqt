from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import json
from settings_manager import SettingsManager


class CalendarWidget(QWidget):

    def __init__(self, dashboard, parent=None):
        super().__init__(parent)

        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)

        # kolor tła kalendarza
        settings_manager = SettingsManager.instance()
        settings_manager.background_color_changed.connect(
            self.update_calendar_background_color)
        background_color = settings_manager.get_background_color()

        self.calendar.setStyleSheet(
            f"background-color: {background_color.name()}")

        self.calendar.clicked[QDate].connect(self.update_events)
        self.calendar.clicked[QDate].connect(self.update_additional_info)

        self.dashboard = dashboard
        self.settings_manager = settings_manager
        # self.settings_manager.filters_changed.connect(self.update_events)

        self.splitter = QSplitter(self)
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.addWidget(self.calendar)
        self.splitter.addWidget(self.dashboard)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.splitter)
        self.setLayout(self.layout)

        self.events = self.load_events_from_file('events.json')
        self.highlight_dates_with_events()
        # self.filters = filters
        # self.dashboard.day_information()

    def load_events_from_file(self, filename):
        with open(filename, 'r') as f:
            events_json = json.load(f)
        self.events = events_json
        return self.events

    def update_events(self, date):
        filters = self.settings_manager.get_filters()
        print(filters)
        # Tutaj powinna być logika filtrowania wydarzeń z listy self.events
        filtered_events = [
            event for event in self.events if event['date'] == date.toString(Qt.ISODate) and event['genre'] in filters]
        self.dashboard.set_events(filtered_events, date)

    def update_special_events(self, date):
        # filtrowanie urodzin, imienin, świąt
        today_events = [
            special_event for special_event in self.events if special_event['date'] == date.toString(Qt.ISODate)]
        print(date.toString(Qt.ISODate))
        self.dashboard.set_special_events(today_events)

    def update_additional_info(self, date):
        self.dashboard.day_information(date)

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

    def update_calendar_background_color(self, color):
        self.calendar.setStyleSheet(f"background-color: {color.name()}")
