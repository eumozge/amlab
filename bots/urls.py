from django.conf.urls import url, include

app_name = 'bots'

urlpatterns = [
    url(r'^', include('bots.core.telegram.urls')),
]
