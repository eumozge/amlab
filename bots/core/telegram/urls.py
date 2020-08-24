from django.conf.urls import url

from .views import APIHookProcessing

app_name = 'telegram'

urlpatterns = [
    url(r"api/v1/bots/telegram/hook/(?P<token_key>[\d\w\D]+)/", APIHookProcessing.as_view()),
]
