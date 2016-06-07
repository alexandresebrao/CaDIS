from django.conf.urls import url

from . import views

app_name = 'pages'
urlpatterns = [
    url(r'^listarprodutos', views.ajax, name='ajax'),
    url(r'^$', views.index, name='index'),
]
