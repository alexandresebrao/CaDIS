from django.conf.urls import url

from . import views

app_name = 'pages'
urlpatterns = [
    url(r'^addcarrinho/(?P<produto>[\w|\W]+)/', views.carrinho),
    url(r'^carrinho/', views.mostrar_carrinho),
    url(r'^limpar_carrinho/', views.limpar_carrinho),
    url(r'^administrador/', views.admin),
    url(r'^finalizar/', views.finalizar),
    url(r'^$', views.index, name='index'),

]
