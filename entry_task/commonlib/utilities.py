from django.core import serializers
import random
import string
import hashlib
import json
from django.http import JsonResponse


from Crypto import Random
from Crypto.Cipher import AES
import base64
from hashlib import md5

BLOCK_SIZE = 16


def pad(data):
    length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + (chr(length)*length).encode()


def unpad(data):
    return data[:-(data[-1] if type(data[-1]) == int else ord(data[-1]))]


def bytes_to_key(data, salt, output=48):
    assert len(salt) == 8, len(salt)
    data += salt
    key = md5(data).digest()
    final_key = key
    while len(final_key) < output:
        key = md5(key + data).digest()
        final_key += key
    return final_key[:output]


def encrypt(message, passphrase):
    salt = Random.new().read(8)
    key_iv = bytes_to_key(passphrase, salt, 32+16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(b"Salted__" + salt + aes.encrypt(pad(message)))


def decrypt(encrypted, passphrase):
    encrypted = base64.b64decode(encrypted)
    assert encrypted[0:8] == b"Salted__"
    salt = encrypted[8:16]
    key_iv = bytes_to_key(passphrase, salt, 32+16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(encrypted[16:]))


def random_string(length=10):
    letters = string.ascii_lowercase + '0123456789'
    return ''.join(random.choice(letters) for i in range(length))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def object_to_json(obj):
    data = serializers.serialize("json", [obj], )
    data = json.loads(data)[0]
    return json.dumps(data)


def make_response(error, status, content=None):
    res = {
        "error": error,
        "status": status,
    }
    if content:
        res["content"] = content
    return JsonResponse(res)

