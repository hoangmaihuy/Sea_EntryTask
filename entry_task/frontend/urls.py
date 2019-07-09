from django.conf.urls import url, include

import views

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^events/$', views.redirect_to_page_1),
    url(r'^events$', views.redirect_to_page_1),
    url(r'^events/(?P<page_id>[0-9]+)/$', views.all_events, name='all_events'),
    url(r'^event/(?P<event_id>[0-9]+)/$', views.event_detail, name='event_detail'),
    url(r'^event/create$', views.event_create, name='event_create'),
]