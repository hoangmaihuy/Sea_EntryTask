import random
from django.core.management.base import BaseCommand
import dateutil
from datetime import datetime
from commonlib.utilities import sha, random_string
import mysql.connector

ENTRIES_NUMBER = 10
DOMAIN = 'http://127.0.0.1:8000'

mydb = mysql.connector.connect(
    user="root",
    password="123456",
    database="event_platform_db"
)
cursor = mydb.cursor()


def random_date():
    return '{0}-{1}-{2}T{3}:{4}:00Z'.format(random.randint(2000, 2030), random.randint(1, 12), random.randint(1, 28),
                                            random.randint(0, 23), random.randint(0, 59))


class Command(BaseCommand):
    help = 'Generate databases'

    def handle(self, *args, **kwargs):

        gen_users()
        gen_events()
        gen_comments()
        gen_likes()
        gen_participants()
        cursor.close()
        mydb.close()


def gen_users():
    print("Generating users...")
    cursor.execute("TRUNCATE user_tab")
    mydb.commit()
    command = (
        "INSERT INTO user_tab "
        "(username, password, salt, role) "
        "VALUES (%s, %s, %s, %s)"
    )
    for user_id in range(1, ENTRIES_NUMBER+1):
        try:
            salt = random_string()
            password = sha(sha("123456")+salt)
            data = ("user_" + str(user_id), password, salt, 0)
            # print("User " + new_user["username"] + " created")
            cursor.execute(command, data)
            mydb.commit()
        except Exception as e:
            print(e)

    try:
        salt = random_string()
        password = sha(sha("123456")+salt)
        data = ("admin", password, salt, 1)
        cursor.execute(command, data)
        mydb.commit()
    except Exception as e:
        print(e)
    print("Finish generating users")


def gen_events():
    print("Generating events...")
    cursor.execute("TRUNCATE event_tab")
    cursor.execute("TRUNCATE event_category_tab")
    mydb.commit()
    event_command = (
        "INSERT INTO event_tab "
        "(title, description, date, location, photo_url, categories) "
        "VALUES (%(title)s, %(description)s, %(date)s, %(location)s, %(photo_url)s, %(categories)s)"
    )
    event_category_command = (
        "INSERT INTO event_category_tab "
        "(event_id, category_name) "
        "VALUES (%s, %s)"
    )
    for event_id in range(1, ENTRIES_NUMBER+1):
        try:
            category_1 = "category_" + str(random.randint(1, ENTRIES_NUMBER))
            category_2 = "category_" + str(random.randint(1, ENTRIES_NUMBER))
            data = {
                "title": "event_" + str(event_id),
                "description": "description for event_" + str(event_id),
                "date": dateutil.parser.parse(random_date()),
                "location": "location of event_" + str(event_id),
                "photo_url": "/static/images/abcd123456.jpg",
                "categories": category_1+','+category_2
            }
            cursor.execute(event_command, data)
            mydb.commit()
            event_id = cursor.lastrowid
            cursor.execute(event_category_command, (event_id, category_1))
            cursor.execute(event_category_command, (event_id, category_2))
            mydb.commit()
            # print("Event " + new_event["title"] + " created")
        except Exception as e:
            print(e)
    print("Finish generating events")


def gen_comments():
    print("Generating comments...")
    cursor.execute("TRUNCATE comment_tab")
    mydb.commit()
    command = (
        "INSERT INTO comment_tab "
        "(event_id, by_user, content, created_time) "
        "VALUES (%(event_id)s, %(by_user)s, %(content)s, %(created_time)s)"
    )
    for _ in range(1, ENTRIES_NUMBER+1):
        event_id = random.randint(1, ENTRIES_NUMBER)
        by_user = "user_" + str(random.randint(1, ENTRIES_NUMBER))
        new_comment = {
            "event_id": event_id,
            "by_user": by_user,
            "content": "User {0} comment event {1}".format(by_user, event_id),
            "created_time": datetime.now()
        }
        try:
            cursor.execute(command, new_comment)
            mydb.commit()
            # print("User {0} comment event {1}".format(by_user, event_id))
        except Exception as e:
            print(e)
    print("Finish generating comments")


def gen_likes():
    print("Generating likes...")
    cursor.execute("TRUNCATE event_like_tab")
    mydb.commit()
    command = (
        "INSERT INTO event_like_tab "
        "(event_id, user_name) "
        "VALUES (%s, %s)"
    )
    for _ in range(1, ENTRIES_NUMBER+1):
        event_id = random.randint(1, ENTRIES_NUMBER)
        user_name = "user_" + str(random.randint(1, ENTRIES_NUMBER))
        try:
            cursor.execute(command, (event_id, user_name))
            mydb.commit()
            # print("User {0} liked event {1}".format(user_id, event_id))
        except Exception as e:
            print(e)
    print("Finish generating likes")


def gen_participants():
    print("Generating participants...")
    cursor.execute("TRUNCATE event_participant_tab")
    mydb.commit()
    command = (
        "INSERT INTO event_participant_tab "
        "(event_id, user_name) "
        "VALUES (%s, %s)"
    )
    for _ in range(1, ENTRIES_NUMBER + 1):
        event_id = random.randint(1, ENTRIES_NUMBER)
        user_name = "user_" + str(random.randint(1, ENTRIES_NUMBER))
        try:
            cursor.execute(command, (event_id, user_name))
            mydb.commit()
            # print("User {0} participated in event {1}".format(user_id, event_id))
        except Exception as e:
            print(e)
    print("Finish generating participants")

