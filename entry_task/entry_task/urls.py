from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include('event_platform_api.urls')),
    url(r'^', include('event_platform.urls')),
    #url(r'^admin$', views.admin, name='admin'),

]