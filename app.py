from flask import Flask, request, render_template
from datetime import datetime

app = Flask(__name__)


TITLE_LIMIT = 30
TEXT_LIMIT = 200


class Event:
    def __init__(self, uid: str, day: datetime, title: str, text: str):
        self.uid = uid
        self.day = day
        self.title = title
        self.text = text


class ClassException(Exception):
    pass


class Action:
    def __init__(self):
        self.db = DataBase()

    def checkup(self, event: Event):
        if len(event.title) > TITLE_LIMIT:
            raise ClassException(f'Title length > max: {TITLE_LIMIT}')
        elif len(event.text) > TEXT_LIMIT:
            raise ClassException(f'Text length > max: {TEXT_LIMIT}')
        elif event.uid in self.db.data.data.keys():
            raise ClassException('You may add just one event for a day')

    def create(self, event: Event):
        self.checkup(event)
        try:
            self.db.create(event)
        except Exception as ex:
            return f'Failed: {ex}'

    def list(self):
        try:
            return self.db.list()
        except Exception as ex:
            return ClassException(f'Failed: {ex}')

    def read(self, uid: str):
        try:
            return self.db.read(uid)
        except Exception as ex:
            return ClassException(f'Failed: {ex}')

    def update(self, uid: str, event: Event):
        self.checkup(event)
        try:
            self.db.update(uid, event)
        except Exception as ex:
            return f'Failed: {ex}'

    def delete(self, uid: str):
        try:
            self.db.delete(uid)
        except Exception as ex:
            return ClassException(f'Failed: {ex}')


class Storage:
    def __init__(self):
        self.data = {}

    def create(self, event: Event):
        try:
            self.data[event.uid] = event
        except (Exception,):
            return ClassException('Failed to create an event')

    def list(self):
        try:
            return self.data.values()
        except (Exception,):
            return ClassException('Failed list events')

    def read(self, event_id: str):
        try:
            return self.data[event_id]
        except (Exception,):
            return ClassException('Event not found')

    def update(self, uid: str, event: Event):
        try:
            self.data[uid] = event
        except (Exception,):
            return ClassException('Failed to update')

    def delete(self, event_id: str):
        try:
            del self.data[event_id]
        except (Exception,):
            return ClassException('Failed to delete')


class DataBase:
    def __init__(self):
        self.data = Storage()

    def create(self, event: Event):
        try:
            self.data.create(event)
        except (Exception,):
            return ClassException('Failed to create an event')

    def list(self):
        try:
            return self.data.list()
        except (Exception,):
            return ClassException('Failed to list events')

    def read(self, event_id: str):
        try:
            return self.data.read(event_id)
        except (Exception,):
            return ClassException('Event not found')

    def update(self, event_id: str, event: Event):
        try:
            self.data.update(event_id, event)
        except (Exception,):
            return ClassException('Failed to update')

    def delete(self, event_id: str):
        try:
            self.data.delete(event_id)
        except (Exception,):
            return ClassException('Failed to delete')


action = Action()


def from_raw_to_event(raw_event: str) -> Event:
    try:
        event_list_data = raw_event.split('|')
        event_id = event_list_data[0].replace('-', '')
        day = datetime.strptime(event_list_data[0], '%Y-%m-%d')
        title = event_list_data[1]
        text = event_list_data[2]
        event = Event(event_id, day, title, text)
        return event
    except Exception:
        raise ClassException('Invalid data entry format')


def to_raw(event: Event):
    return f'{event.day.strftime("%Y-%m-%d")}|{event.title}|{event.text}'


@app.route('/api/v1/')
def main():
    return render_template('main.html')


@app.route('/api/v1/event/', methods=['POST'])
def create():
    try:
        get_data = request.get_data().decode('utf-8')
        event = from_raw_to_event(get_data)
        action.create(event)
        return f'New event created: {event.title}. Date:' \
               f' {event.day.strftime("%Y-%m-%d")}. id: {event.uid}'
    except Exception as ex:
        return f'Failed: {ex}'


@app.route('/api/v1/event/', methods=['GET'])
def lst():
    try:
        raw = ''
        for elem in action.list():
            raw += to_raw(elem) + '\n'
        return raw
    except Exception as ex:
        return f'Failed: {ex}'


@app.route('/api/v1/event/<uid>/', methods=['GET'])
def read(uid: str):
    try:
        result = action.read(uid)
        return to_raw(result)
    except Exception as ex:
        return f'Failed: {ex}'


@app.route('/api/v1/event/<uid>/', methods=['PUT'])
def update(uid: str):
    try:
        get_data = request.get_data().decode('utf-8')
        event = from_raw_to_event(get_data)
        action.update(uid, event)
        return f'Event id: {uid} updated'
    except Exception as ex:
        return f'Failed: {ex}'


@app.route('/api/v1/event/<uid>/', methods=['DELETE'])
def delete(uid: str):
    try:
        action.delete(uid)
        return f'Event id:{uid} deleted'
    except Exception as ex:
        return f'Failed: {ex}'


if __name__ == '__main__':
    app.run(debug=True)
