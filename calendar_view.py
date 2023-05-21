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
        self.my_palette = self.calendar.palette()

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
        settings_manager.filters_changed.connect(
            self.unhighlight_deleted_dates)

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

    def attach_color_to_type(self, type):
        print(type)
        if type == "Urodziny":
            return Qt.red
        elif type == "Imieniny":
            return Qt.blue
        elif type == "Święta":
            return Qt.yellow
        elif type == "Kulturalne":
            return Qt.green
        elif type == "Biznesowe":
            return Qt.magenta
        elif type == "Naukowe":
            return Qt.darkCyan
        elif type == "Inne":
            return Qt.darkYellow
        else:
            return Qt.white

    def highlight_dates_with_events(self):
        print("highlight_dates_with_events")
        filters = self.settings_manager.get_filters()
        # Tworzenie formatu dla dat z wydarzeniami
        date_format = QTextCharFormat()

        # Dodawanie formatu dla dat z wydarzeniami
        for event in self.events:
            print(event['genre'])
            print(filters)
            if event['genre'] in filters:
                date_format.setBackground(
                    self.attach_color_to_type(event['genre']))
                event_date = QDate.fromString(event['date'], Qt.ISODate)
                self.calendar.setDateTextFormat(event_date, date_format)

    def unhighlight_deleted_date(self, event):
        # Tworzenie formatu dla usuniętej daty
        date_format = QTextCharFormat()
        date_format.setBackground(QColor(255, 255, 240))

        # Dodawanie formatu dla usuniętej daty
        event_date = QDate.fromString(event['date'], Qt.ISODate)
        self.calendar.setDateTextFormat(event_date, date_format)

    def unhighlight_deleted_dates(self, filters):
        self.highlight_dates_with_events()
        for event in self.events:
            if event['genre'] not in filters:
                self.unhighlight_deleted_date(event)

    def update_calendar_background_color(self, color):
        self.calendar.setStyleSheet(f"background-color: {color.name()}")
        self.dashboard.setStyleSheet(f"background-color: {color.name()}")
        self.my_palette.setColor(QPalette.Window, color)
        self.calendar.setPalette(self.my_palette)
