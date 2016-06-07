# DJANGO
from django.shortcuts import render

# DataBase
from cassandra.cluster import Cluster
import redis


# Create your views here.
def index(request):
    #CONNECT TO PYTHON - CASSANDRA#
    cluster = Cluster()
    session = cluster.connect('ecommerce')
    rows = session.execute('SELECT codigo, descricao, preco FROM produto')
    context = {'rows': rows}
    return render(request, 'base.html', context)


def carrinho(request):
    context = {}
    return render(request, 'polls/index.html', context)


def fecharpedido(request):
    context = {}
    return render(request, 'polls/index.html', context)


def ajax(request):
    context = {}
    return render(request, 'ajax.html', context)
