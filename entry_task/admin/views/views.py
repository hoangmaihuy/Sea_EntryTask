from commonlib.constant import UNAUTHORIZED, STATIC_URL, BAD_REQUEST, OK
from commonlib.utilities import make_response, random_string
from commonlib import db_connector
from commonlib.decorator import parse_user
from jsonschema import validate
from jsonschema.exceptions import ValidationError

@parse_user
def create_event(user, data):
    if user["role"] != 1:
        return make_response(UNAUTHORIZED, "Unauthorized!")
    schema = {
        "type": "object",
        "required": ["title", "description", "date", "location", "photo_url"],
        "properties": {
            "title": {"type": "string"},
            "description": {"type": "string"},
            "date": {"type": "string", "format": "date-time"},
            "location": {"type": "string"},
            "photo_url": {"type": "string"}
        }
    }
    try:
        validate(data, schema)
        event = db_connector.new_event(user["name"], data)
        return make_response(OK, "ok", event)
    except ValidationError:
        return make_response(BAD_REQUEST, "Bad request")


def upload_photo(request):
    headers = request.META
    if 'HTTP_TOKEN' not in headers:
        return make_response(UNAUTHORIZED, "Unauthorized!")
    token = headers.get('HTTP_TOKEN')
    user = db_connector.get_session(token)
    if user["role"] != 1:
        return make_response(UNAUTHORIZED, "Unauthorized!")
    try:
        image = request.FILES["image"]
        ext = str(image.name).split('.')[-1]
        name = random_string() + '.' + ext
        url = '/static/images/' + name
        with open(STATIC_URL + 'images/' + name, 'wb+') as destination:
            destination.write(image.read())
        return make_response(0, "ok", {"photo_url": url})
    except Exception as e:
        return make_response(BAD_REQUEST, str(e))
