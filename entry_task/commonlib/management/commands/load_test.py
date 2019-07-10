from django.core.management.base import BaseCommand
from commonlib.utilities import encrypt, sha
import requests
import random
import timeit


USERS_NUMBER = 500
ENTRIES_NUMBER = 1000000
DOMAIN = 'http://172.16.153.128'
ENDPOINT = '/api/login'


class Command(BaseCommand):
    help = 'Load test Login API'

    def handle(self, *args, **kwargs):
        start_time = timeit.default_timer()
        error_count = 0
        success_count = 0
        for _ in range(USERS_NUMBER):
            username = "user_" + str(random.randint(1, USERS_NUMBER))
            password = sha("123456")
            response = requests.post(DOMAIN+ENDPOINT, json={"username": username})
            if response.status_code == 200:
                data = response.json()
                key = str(data["content"].get("key"))
                encrypted_password = encrypt(password, key)
                response = requests.post(DOMAIN+ENDPOINT, json={"username": username, "password": encrypted_password})
                if response.status_code == 200:
                    success_count += 1
                    data = response.json()
                    #print(data.get("status"))
                else:
                    error_count += 1
            else:
                error_count += 1
        stop_time = timeit.default_timer()
        print("time: {}".format(stop_time-start_time))
        print("error: {}".format(error_count))
        print("success: {}".format(success_count))

