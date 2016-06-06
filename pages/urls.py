from django.conf.urls import url

from . import views

app_name = 'pages'
urlpatterns = [
    url(r'^produtos', views.index, name='index'),
    url(r'^$', views.index, name='index'),
]
