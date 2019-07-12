from locust import HttpLocust, TaskSet, task
import random
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
import base64
from hashlib import md5

USERS_NUMBER = 500
DOMAIN = 'http://127.0.0.1:8000'
ENDPOINT = '/api/login'
BLOCK_SIZE = 16
DEFAULT_PASSWORD = "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


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


class LoginBehavior(TaskSet):

    @task(1)
    def get_key(self):
        username = "user_" + str(random.randint(1, USERS_NUMBER))
        with self.client.post(ENDPOINT, json={"username": username}, catch_response=True) as response:
            try:
                data = response.json()
                key = str(data["content"].get("key"))
                try:
                    password = encrypt(DEFAULT_PASSWORD, key)
                    with self.client.post(ENDPOINT, json={"username": username, "password": password}, catch_response=True) as response:
                        pass
                except Exception as e:
                    print(str(e))
            except Exception as e:
                print(str(e))


class MyLocust(HttpLocust):
    task_set = LoginBehavior
    stop_timeout = 3

