from django.conf.urls import url

from battle import views

urlpatterns = [
    url(r'^battle/(?P<battle_id>[0-9]+)', views.detail, name='detail'),
    url(r'^', views.index, name='index')
]
