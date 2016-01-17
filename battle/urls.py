from django.conf.urls import url

from battle import views

urlpatterns = [
    url(r'^api/battle/(?P<battle_id>[0-9]+)', views.api_detail, name='api_detail'),
    url(r'^battle/(?P<battle_id>[0-9]+)', views.detail, name='detail'),
    url(r'^', views.index, name='index')
]
