from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import icalendar
import json
from datetime import date


class CalendarParser():

    def __init__(self, selected_events, filename):
        self.events = selected_events
        self.filename = filename
        self.i_calendar = icalendar.Calendar()

    def load_from_icalendar(self):
        with open(self.filename, 'r') as f:
            calendar_file = f.read()
        self.i_calendar = icalendar.Calendar.from_ical(calendar_file)
        for component in self.i_calendar.walk():
            if component.name == "VEVENT":
                event = {
                    'title': component.get('summary'),
                    'description': '',
                    'date': component.get('dtstart').dt.isoformat(),
                    'time': '',
                    'genre': 'Inne'
                }
                self.events.append(event)
        return self.events

    def create_icalendar(self):
        for event in self.events:
            event_ical = icalendar.Event()
            event_ical.add('summary', event['title'])
            event_ical.add('dtstart', date.fromisoformat(event['date']))
            event_ical.add('dtend', date.fromisoformat(event['date']))
            self.i_calendar.add_component(event_ical)

    def export_events_to_file(self):
        self.create_icalendar()
        with open(self.filename, 'wb') as f:
            f.write(self.i_calendar.to_ical())
