from __future__ import unicode_literals
from .models import *
from .utilities import sha, random_string
from .constant import TOKEN_TIME
from django.core.cache import cache
import dateutil.parser
from django.forms.models import model_to_dict


def get_user(username):
    user = cache.get(username)
    if user:
        return user
    try:
        user = User.objects.get(username=username)
        cache.set(username, user)
        return user
    except User.DoesNotExist:
        return None


def new_user(username, password):
    salt = random_string()
    password_hash = sha(password + salt)
    User.objects.create(username=username, password=password_hash, salt=salt, role=0)


def new_session(user):
    token = random_string(64)
    cache.set(token, {"id": user.id, "role": user.role, "name": user.username}, TOKEN_TIME)
    return {"token": token}


def get_session(token):
    return cache.get(token)


def get_all_events(offset, size):
    events = Event.objects.values('id')[offset:offset+size]
    events = [event["id"] for event in events]
    return events


def get_events_by_category(offset, size, category):
    events = EventCategoryMap.objects.filter(category_name=category).values('event_id')[offset:offset+size]
    events = [event["event_id"] for event in events]
    return events


def get_events_by_date(offset, size, start_date, end_date):
    start_date = dateutil.parser.parse(start_date)
    end_date = dateutil.parser.parse(end_date)
    events = Event.objects.filter(date__gte=start_date, date__lte=end_date).values('id')[offset:offset+size]
    events = [event["id"] for event in events]
    return events


def get_event(event_id):
    try:
        event = Event.objects.get(id=event_id)
        return model_to_dict(event)
    except Event.DoesNotExist:
        return None


def add_comment(user_name, event_id, content):
    Comment.objects.create(event_id=event_id, by_user=user_name, content=content)


def get_comments(event_id, offset, size):
    comments = Comment.objects.filter(event_id=event_id).all()[offset:offset+size]
    comments = [{"by_user": comment.by_user, "content": comment.content} for comment in comments]
    return comments


def add_participant(user_name, event_id):
    if EventParticipantMap.objects.filter(event_id=event_id, user_name=user_name).exists():
        return False
    EventParticipantMap.objects.create(event_id=event_id, user_name=user_name)
    return True


def get_participants(event_id, offset, size):
    participants = EventParticipantMap.objects.filter(event_id=event_id).values('user_name')[offset:offset+size]
    participants = [participant["user_name"] for participant in participants]
    return participants


def add_like(user_name, event_id):
    if EventLikeMap.objects.filter(event_id=event_id, user_name=user_name).exists():
        return False
    EventLikeMap.objects.create(event_id=event_id, user_name=user_name)
    return True


def get_likes(event_id, offset, size):
    likes = EventLikeMap.objects.filter(event_id=event_id).values('user_name')[offset:offset+size]
    likes = [like["user_name"] for like in likes]
    return likes


def new_event(user_name, data):
    event = Event.objects.create(
        title=data["title"],
        description=data["description"],
        date=dateutil.parser.parse(data["date"]),
        location=data["location"],
        created_by=user_name,
        photo_url=data["photo_url"],
        categories=','.join(data["categories"])
    )
    event_id = event.id
    for category_name in data["categories"]:
        EventCategoryMap.objects.create(event_id=event_id, category_name=category_name)
    return model_to_dict(event)
