from django.conf.urls import url

from . import views

app_name = 'pages'
urlpatterns = [
    url(r'^/addcarrinho/(?P<produto>\w+)/', views.carrinho),
    url(r'^/carrino/', views.mostrar_carrinho),
    url(r'^$', views.index, name='index'),
]
