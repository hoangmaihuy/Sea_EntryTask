import random
from django.core.management.base import BaseCommand
from event_platform.models import *
import dateutil
import string
import hashlib

ENTRIES_NUMBER = 1000000
DOMAIN = 'http://127.0.0.1:8000'


def random_date():
    return '{0}-{1}-{2}T{3}:{4}:00Z'.format(random.randint(2000, 2030), random.randint(1, 12), random.randint(1, 28),
                                            random.randint(0, 23), random.randint(0, 59))


def random_string(length=10):
    letters = string.ascii_lowercase + '0123456789'
    return ''.join(random.choice(letters) for i in range(length))


def encrypt_string(hash_string):
    return hashlib.sha256(hash_string).hexdigest()


class Command(BaseCommand):
    help = 'Generate databases'

    def handle(self, *args, **kwargs):
        gen_users()
        gen_events()
        gen_categories()
        gen_comments()
        gen_likes()
        gen_participants()
        gen_sessions()


def gen_users():
    print("Generating users...")
    for user_id in range(1, ENTRIES_NUMBER+1):
        try:
            salt = random_string()
            password = encrypt_string("123456" + salt)
            new_user = {
                "username": "user_" + str(user_id),
                "password": password,
                "salt" : salt,
                "role": 0
            }
            User.objects.create(**new_user)
            # print("User " + new_user["username"] + " created")
        except Exception as e:
            print(e)

    try:
        salt = random_string()
        password = encrypt_string("123456" + salt)
        User.objects.create(
            username="admin",
            password=password,
            salt=salt,
            role=1
        )
        # print("User admin created")
    except Exception as e:
        print(e)
    print("Finish generating users")


def gen_events():
    print("Generating events...")
    for event_id in range(1, ENTRIES_NUMBER+1):
        try:
            new_event = {
                "title": "event_" + str(event_id),
                "description": "description for event_" + str(event_id),
                "date": dateutil.parser.parse(random_date()),
                "location": "location of event_" + str(event_id),
                "created_by": 1,
                "photo_url": ""
            }
            Event.objects.create(**new_event)
            # print("Event " + new_event["title"] + " created")
        except Exception as e:
            print(e)
    print("Finish generating events")


def gen_categories():
    print("Generating categories...")
    # create new categories
    for category_id in range(1, ENTRIES_NUMBER+1):
        try:
            new_category = {
                "category_name": "category_" + str(category_id)
            }
            Category.objects.create(**new_category)
            # print("Category " + new_category["category_name"] + " created")
        except Exception as e:
            print(e)

    # map categories with events
    for _ in range(1, ENTRIES_NUMBER+1):
        try:
            event_id = random.randint(1, ENTRIES_NUMBER)
            category_id = random.randint(1, ENTRIES_NUMBER)
            EventCategoryMap.objects.create(event_id=event_id, category_id=category_id)
            # print("Event {0} added category {1}".format(event_id, category_id))
        except Exception as e:
            print(e)
    print("Finish generating categories")


def gen_comments():
    print("Generating comments...")
    for _ in range(1, ENTRIES_NUMBER+1):
        event_id = random.randint(1, ENTRIES_NUMBER)
        by_user = random.randint(1, ENTRIES_NUMBER)
        new_comment = {
            "event_id": event_id,
            "by_user": by_user,
            "content": "User {0} comment event {1}".format(by_user, event_id)
        }
        try:
            Comment.objects.create(**new_comment)
            # print("User {0} comment event {1}".format(by_user, event_id))
        except Exception as e:
            print(e)
    print("Finish generating comments")


def gen_likes():
    print("Generating likes...")
    for _ in range(1, ENTRIES_NUMBER+1):
        event_id = random.randint(1, ENTRIES_NUMBER)
        user_id = random.randint(1, ENTRIES_NUMBER)
        try:
            EventLikeMap.objects.create(event_id=event_id, user_id=user_id)
            # print("User {0} liked event {1}".format(user_id, event_id))
        except Exception as e:
            print(e)
    print("Finish generating likes")


def gen_participants():
    print("Generating participants...")
    for _ in range(1, ENTRIES_NUMBER + 1):
        event_id = random.randint(1, ENTRIES_NUMBER)
        user_id = random.randint(1, ENTRIES_NUMBER)
        try:
            EventParticipantMap.objects.create(event_id=event_id, user_id=user_id)
            # print("User {0} participated in event {1}".format(user_id, event_id))
        except Exception as e:
            print(e)
    print("Finish generating participants")


def gen_sessions():
    print("Generating sessions...")
    for _ in range(1, ENTRIES_NUMBER+1):
        user_id = random.randint(1, ENTRIES_NUMBER)
        token = random_string(64)
        try:
            Session.objects.create(user_id=user_id, token=token)
            # print("New session of user " + str(user_id))
        except Exception as e:
            print(e)
    print("Finish generating sessions")

