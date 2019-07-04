from django.core import serializers
import random
import string
import hashlib
import json


def random_string(length=10):
    letters = string.ascii_lowercase + '0123456789'
    return ''.join(random.choice(letters) for i in range(length))


def encrypt_string(hash_string):
    return hashlib.sha256(hash_string).hexdigest()


def object_to_json(obj):
    data = serializers.serialize("json", [obj], )
    data = json.loads(data)[0]
    return json.dumps(data)


def list_to_json(list):
    data = serializers.serialize("json", list)
    return data


def make_response(error, status, content=None):
    res = {
        "error": error,
        "status": status,
    }
    if content:
        res["content"] = content
    return res

