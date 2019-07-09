from django.conf.urls import url

import views

urlpatterns = [
    url(r'^login$', views.login, name="api/login"),
    url(r'^events$', views.event_get_list, name="api/events"),
    url(r'^event$', views.event_get_detail, name="api/event"),
    url(r'^event/get_comments$', views.event_get_comments, name='api/event/get_comments'),
    url(r'^event/add_comment$', views.event_add_comment, name='api/event/add_comment'),
    url(r'^event/add_like$', views.event_add_like, name='api/event/add_like'),
    url(r'^event/get_likes$', views.event_get_likes, name='api/event/get_likes'),
    url(r'^event/get_participants$', views.event_get_participants, name='api/event/get_participants'),
    url(r'^event/add_participant$', views.event_add_participant, name='api/event/participate'),
]