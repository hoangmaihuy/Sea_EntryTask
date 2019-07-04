from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf.urls import url
from django.forms import ModelForm
from event_platform_api.views import *
from .models import *
import requests
import os

BASE_DIR = os.path.realpath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates/')


def login(request):
    if request.method == 'POST':
        print(request.body)
        return HttpResponse("ok")
    else:
        return render(request, TEMPLATE_DIR + 'login.html')


def all_events(request, page_id):
    return render(request, TEMPLATE_DIR + 'events.html', {'page_id': page_id})


def event_detail(request, event_id):
    return render(request, TEMPLATE_DIR + 'event_detail.html', {'event_id': event_id})


def event_create(request):
    return render(request, TEMPLATE_DIR + 'event_create.html')


def redirect_to_page_1(request):
    return redirect('/events/1')
