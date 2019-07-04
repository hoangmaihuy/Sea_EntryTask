from __future__ import unicode_literals
from django.http import JsonResponse
from event_platform.models import *
from event_platform.utilities import *
from django.forms.models import model_to_dict
import dateutil.parser
import os
from django.core import serializers
from django.core.cache import cache

# admin token: amzbb8ha20uvbw4f7grsyeu7xkc170k9oaboqm6n0s3e2nqdm2cqnvkv92x60nnj
# test token : h1lrn1i75j24mj5oao3vaptze4vhftmsos4qakje4ryeriq583cf05aiszr0thol

PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))
STATIC_URL = PROJECT_PATH + '/event_platform/' + '/static/'


def get_user_by_id(user_id):
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        return None


def get_user_id_by_token(token):
    user_id = cache.get(token)
    if not user_id:
        return None
    else:
        return user_id


def auth(headers):
    if 'HTTP_TOKEN' not in headers:
        return -1
    else:
        token = headers.get('HTTP_TOKEN')
        user_id = cache.get(token)
        if not user_id:
            return -1
        else:
            return get_user_by_id(user_id).role


def register(request):
    req = json.loads(request.body)
    try:
        username = req["username"]
        password = req["password"]
        salt = random_string()
        hash_password = encrypt_string(password + salt)
        try:
            User.objects.get(username=username)
            return JsonResponse(make_response(3, "Username has been used"))
        except User.DoesNotExist:
            user = User(username=username, password=hash_password, salt=salt, role=0)
            user.save()
            return JsonResponse(make_response(0, "User {0} has been created".format(username)))
    except:
        return JsonResponse(make_response(2, "Bad request"))


def login(request):
    req = json.loads(request.body)
    try:
        username = req["username"]
        password = req["password"]
        try:
            user = User.objects.get(username=username)
            hash_password = encrypt_string(password + user.salt)
            if hash_password != user.password:
                return JsonResponse(make_response(3, "Password Incorrect!"))
            else:
                token = random_string(64)
                cache.set(token, user.id, 7200) # token valid for 2 hours 
                return JsonResponse(make_response(0, "Login successfully!", {"token": token}))
        except User.DoesNotExist:
            return JsonResponse(make_response(3, "User does not exist!"))
    except:
        return JsonResponse(make_response(2, "Bad request"))


def event_get_list(request):
    headers = request.META
    if auth(headers) == -1:
        return JsonResponse(make_response(1, "Unauthorized"))
    req = json.loads(request.body)
    offset = req.get('offset')
    size = req.get('size')
    category = req.get('category')
    start_date = req.get('start_date')
    end_date = req.get('end_date')
    if category:
        try:
            category_id = Category.objects.get(category_name=category).id
            events_list = EventCategoryMap.objects.filter(category_id=category_id)[offset:offset+size]
            res = [event.event_id for event in events_list]
        except Category.DoesNotExist:
            return JsonResponse(make_response(0, "OK"))
    elif start_date and end_date:
        start_date = dateutil.parser.parse(start_date)
        end_date = dateutil.parser.parse(end_date)
        events_list = Event.objects.filter(date__gte=start_date, date__lte=end_date)[offset:offset+size]
        res = [event.id for event in events_list]
    else:
        events_list = Event.objects.all()[offset:offset+size]
        res = [event.id for event in events_list]
        print(res)
    return JsonResponse(make_response(0, "OK", res))


def event_get_detail(request):
    if auth(request.META) == -1:
        return JsonResponse(make_response(1, "Unauthorized"))
    try:
        req = json.loads(request.body)
        event_id = req["event_id"]
        try:
            event = Event.objects.get(id=event_id)
            res = model_to_dict(event)
            res["date"] = res["date"].strftime("%X %x")
            return JsonResponse(make_response(0, "OK", res))
        except Event.DoesNotExist:
            return JsonResponse(make_response(3, "Event does not exist"))
    except:
        return JsonResponse(make_response(2, "Bad request"))


def event_create(request):
    headers = request.META
    if auth(headers) != 1:
        return JsonResponse(make_response(1, "Unauthorized"))
    try:
        req = json.loads(request.body)
        new_event = Event.objects.create(
            title=req["title"],
            description=req["description"],
            date=dateutil.parser.parse(req["date"]),
            location=req["location"],
            created_by=get_user_id_by_token(headers.get('HTTP_TOKEN')),
            photo_url=req["photo_url"]
        )
        event_id = new_event.id
        for category_name in req["categories"]:
            category_id = Category.objects.get_or_create(category_name=category_name)[0].id
            EventCategoryMap.objects.create(event_id=event_id, category_id=category_id)
        res = model_to_dict(new_event)
        return JsonResponse(make_response(0, "OK", res))
    except Exception as e:
        print(e)
        return JsonResponse(make_response(2, "Bad request"))


def event_add_comment(request):
    headers = request.META
    if auth(headers) == -1:
        return JsonResponse(make_response(1, "Unauthorized"))
    try:
        req = json.loads(request.body)
        user_id = get_user_id_by_token(headers['HTTP_TOKEN'])
        event_id = req['event_id']
        new_comment = Comment(event_id=event_id, by_user=user_id, content=req['content'])
        try:
            Event.objects.get(id=event_id)
            new_comment.save()
            return JsonResponse(make_response(0, "Comment added to event {0}".format(event_id), model_to_dict(new_comment)))
        except Event.DoesNotExist:
            return JsonResponse(make_response(3, "Event {0} does not exist".format(event_id)))
    except:
        return JsonResponse(make_response(2, "Bad request"))


def event_get_comments(request):
    headers = request.META
    if auth(headers) == -1:
        return JsonResponse(make_response(1, "Unauthorized"))
    try:
        req = json.loads(request.body)
        event_id = req["event_id"]
        try:
            Event.objects.get(id=event_id)
            comments = Comment.objects.filter(event_id=event_id)
            res = [model_to_dict(comment) for comment in comments]
            for comment in res:
                comment["by_user"] = User.objects.get(id=comment["by_user"]).username
            return JsonResponse(make_response(0, "OK", res))
        except Event.DoesNotExist:
            return JsonResponse(make_response(3, "Event {0} does not exist".format(event_id)))
    except:
        return JsonResponse(make_response(2, "Bad request"))


def event_add_participant(request):
    headers = request.META
    if auth(headers) == -1:
        return JsonResponse(make_response(1, "Unauthorized"))
    try:
        req = json.loads(request.body)
        event_id = req['event_id']
        try:
            Event.objects.get(id=event_id)
            user_id = get_user_id_by_token(headers['HTTP_TOKEN'])
            try:
                EventParticipantMap.objects.get(event_id=event_id, user_id=user_id)
                return JsonResponse(
                    make_response(3, "You already participated in this event"))
            except EventParticipantMap.DoesNotExist:
                EventParticipantMap.objects.create(event_id=event_id, user_id=user_id)
                return JsonResponse(
                    make_response(0, "User {0} participated in event {1}".format(user_id, event_id)))
        except Event.DoesNotExist:
            return JsonResponse(make_response(3, "Event {0} does not exist".format(event_id)))
    except:
        return JsonResponse(make_response(2, "Bad request"))


def event_get_participants(request):
    headers = request.META
    if auth(headers) == -1:
        return JsonResponse(make_response(1, "Unauthorized"))
    try:
        req = json.loads(request.body)
        event_id = req['event_id']
        try:
            Event.objects.get(pk=event_id)
            participants = EventParticipantMap.objects.filter(event_id=event_id)
            res = []
            for participant in participants:
                res.append(User.objects.get(id=participant.user_id).username)
            return JsonResponse(make_response(0, "OK", res))
        except Event.DoesNotExist:
            return JsonResponse(make_response(3, "Event {0} does not exist".format(event_id)))
    except:
        return JsonResponse(make_response(2, "Bad request"))


def event_add_like(request):
    headers = request.META
    if auth(headers) == -1:
        return JsonResponse(make_response(1, "Unauthorized"))
    try:
        req = json.loads(request.body)
        event_id = req['event_id']
        try:
            Event.objects.get(pk=event_id)
            user_id = get_user_id_by_token(headers['HTTP_TOKEN'])
            try:
                EventLikeMap.objects.get(event_id=event_id, user_id=user_id)
                return JsonResponse(
                    make_response(3, "You already liked this event"))
            except EventLikeMap.DoesNotExist:
                EventLikeMap.objects.create(event_id=event_id, user_id=user_id)
                return JsonResponse(make_response(0, "User {0} liked event {1}".format(user_id, event_id)))
        except Event.DoesNotExist:
            return JsonResponse(make_response(3, "Event {0} does not exist".format(event_id)))
    except:
        return JsonResponse(make_response(2, "Bad request"))


def event_get_likes(request):
    headers = request.META
    if auth(headers) == -1:
        return JsonResponse(make_response(1, "Unauthorized!"))
    try:
        req = json.loads(request.body)
        event_id = req['event_id']
        try:
            Event.objects.get(pk=event_id)
            likes = EventLikeMap.objects.filter(event_id=event_id)
            res = []
            for like in likes:
                res.append(User.objects.get(id=like.user_id).username)
            return JsonResponse(make_response(0, "OK", res))
        except Event.DoesNotExist:
            return JsonResponse(make_response(3, "Event {0} does not exist".format(event_id)))
    except:
        return JsonResponse(make_response(2, "Bad request"))


def event_get_categories(request):
    headers = request.META
    if auth(headers) == -1:
        return JsonResponse(make_response(1, "Unauthorized!"))
    try:
        req = json.loads(request.body)
        event_id = req['event_id']
        categories = EventCategoryMap.objects.filter(event_id=event_id)
        res = []
        for category in categories:
            res.append(Category.objects.get(id=category.category_id).category_name)
        return JsonResponse(make_response(0, "OK", res))
    except:
        return JsonResponse(make_response(2, "Bad request"))


def upload(request):
    headers = request.META
    if auth(headers) == -1:
        return JsonResponse(make_response(1, "Unauthorized!"))
    try:
        image = request.FILES["image"]
        with open(STATIC_URL + '/images/' + image.name, 'wb+') as destination:
            destination.write(image.read())
        return JsonResponse(make_response(0, "ok", {"photo_url": "/static/images/"+image.name}))
    except Exception as e:
        print(e)