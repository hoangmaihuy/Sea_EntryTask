from __future__ import unicode_literals
from commonlib import db_connector
from commonlib.utilities import make_response, sha, random_string, decrypt
from commonlib.constant import OK, BAD_REQUEST
from commonlib.decorator import parse_event, parse_user, validate_username_password, validate_offset_size
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import json
from django.core.cache import cache


def login(request):
    schema = {
        "type": "object",
        "required": ["username"],
        "properties": {
            "username": {"type": "string"},
            "password": {"type": "string"}
        }
    }
    data = json.loads(request.body)
    try:
        validate(data, schema)
        username = data.get('username')
        password = data.get('password')
        key = cache.get(username+"_key")
        if key:
            cache.delete(username+"_key")
            if not password:
                return make_response(BAD_REQUEST, "Bad request")
            user = db_connector.get_user(username)
            salt = user.salt
            raw_password = decrypt(password, key)
            hash_password = sha(raw_password+salt)
            if hash_password != user.password:
                return make_response(BAD_REQUEST, "Password Incorrect")
            return make_response(OK, "Login Successfully", db_connector.new_session(user))
        else:
            user = db_connector.get_user(username)
            if not user:
                return make_response(BAD_REQUEST, "User does not exist!")
            key = random_string(32)
            cache.set(username+"_key", key, 60)
            return make_response(OK, "ok", {"key": key})
    except ValidationError:
        return make_response(BAD_REQUEST, "Bad request")


@parse_user
def event_get_list(user, data):
    schema = {
        "type": "object",
        "required": ["offset", "size"],
        "properties": {
            "offset": {"type": "number", "minimum": 0},
            "size": {"type": "number", "maximum": 100},
            "start_date": {"type": "string", "format": "date-time"},
            "end_date": {"type": "string", "format": "date-time"},
            "category": {"type": "string"}
        }
    }
    try:
        validate(data, schema)
        offset = data.get('offset')
        size = data.get('size')
        category = data.get('category')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if category:
            events_list = db_connector.get_events_by_category(offset, size, category)
        elif start_date and end_date:
            events_list = db_connector.get_events_by_date(offset, size, start_date, end_date)
        else:
            events_list = db_connector.get_all_events(offset, size)
        return make_response(OK, "ok", events_list)
    except ValidationError:
        return make_response(BAD_REQUEST, "Bad request!")


@parse_user
@parse_event
def event_get_detail(user, event, data):
    return make_response(OK, "ok", event)


@parse_user
@parse_event
def event_add_comment(user, event, data):
    content = data.get("content")
    if (not content) or (content and not isinstance(content, basestring)):
        return make_response(BAD_REQUEST, "Bad request")
    db_connector.add_comment(user["name"], event["id"], content)
    return make_response(OK, "Comment added to event {0}".format(event["id"]))


@parse_user
@parse_event
@validate_offset_size
def event_get_comments(user, event, data):
    comments = db_connector.get_comments(event["id"], data.get('offset'), data.get('size'))
    return make_response(OK, "ok", comments)


@parse_user
@parse_event
def event_add_participant(user, event, data):
    if not db_connector.add_participant(user["name"], event["id"]):
        return make_response(BAD_REQUEST, "You already participated in this event")
    return make_response(OK, "User {0} participated in event {1}".format(user["name"], event["id"]))


@parse_user
@parse_event
@validate_offset_size
def event_get_participants(user, event, data):
    participants = db_connector.get_participants(event["id"], data.get('offset'), data.get('size'))
    return make_response(OK, "ok", participants)


@parse_user
@parse_event
def event_add_like(user, event, data):
    if not db_connector.add_like(user["name"], event["id"]):
        return make_response(BAD_REQUEST, "You already liked this event")
    return make_response(OK, "User {0} liked in event {1}".format(user["name"], event["id"]))


@parse_user
@parse_event
@validate_offset_size
def event_get_likes(user, event, data):
    likes = db_connector.get_likes(event["id"], data.get('offset'), data.get('size'))
    return make_response(OK, "ok", likes)


