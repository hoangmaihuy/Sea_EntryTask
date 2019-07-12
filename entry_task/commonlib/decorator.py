import json
from .utilities import make_response
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from .constant import BAD_REQUEST, UNAUTHORIZED
import db_connector
from commonlib.schema import event_schema, offset_size_schema


def parse_user(func):
    def _func(request):
        headers = request.META
        if 'HTTP_TOKEN' not in headers:
            return make_response(UNAUTHORIZED, "Unauthorized!")
        token = headers.get('HTTP_TOKEN')
        user = db_connector.get_session(token)
        data = json.loads(request.body)
        return func(user, data)
    return _func


def parse_event(func):
    def _func(user, data):
        try:
            validate(data, event_schema)
            event_id = data.get("event_id")
            event = db_connector.get_event(event_id)
            if not event:
                return make_response(BAD_REQUEST, "Event does not exist")
            return func(user, event, data)
        except ValidationError:
            return make_response(BAD_REQUEST, "event_id is not a number")
    return _func


def validate_offset_size(func):
    def _func(user, event, data):

        try:
            validate(data, offset_size_schema)
            return func(user, event, data)
        except ValidationError:
            return make_response(BAD_REQUEST, "Bad request")
    return _func
