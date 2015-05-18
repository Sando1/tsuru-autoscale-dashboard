from django.conf.urls import include, url


urlpatterns = [
    url(r'^$', include('index.urls')),
    url(r'^datasource/', include('datasource.urls')),
    url(r'^alarm/', include('alarm.urls')),
    url(r'^action/', include('action.urls')),
]
