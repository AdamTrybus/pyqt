import random
import json
from datetime import datetime, timedelta

events = []
for i in range(10):
    event_date = datetime.now() - timedelta(days=random.randint(1, 30))
    event_time = datetime.strptime(f"{random.randint(8, 18)}:{random.choice([0, 30])}", "%H:%M").time()
    event_title = f"Event {i+1}"
    event = {
        "date": event_date.strftime("%Y-%m-%d"),
        "time": event_time.strftime("%H:%M"),
        "title": event_title
    }
    events.append(event)

with open("events.json", "w") as f:
    json.dump(events, f)
