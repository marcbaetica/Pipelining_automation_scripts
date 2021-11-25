from json import JSONEncoder


class DatetimeEncoder(JSONEncoder):
    def default(self, o):
        return str(o)
