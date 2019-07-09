from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include('api.urls')),
    url(r'^admin/', include('admin.urls')),
    url(r'^', include('frontend.urls')),
]