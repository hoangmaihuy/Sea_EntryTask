from django.conf.urls import url

import views

urlpatterns = [
    url(r'^create_event$', views.create_event, name="api/create_event"),
    url(r'^upload_photo$', views.upload_photo, name="api/upload_photo"),
]