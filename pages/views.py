#DJANGO
from django.shortcuts import render

#DataBase
from cassandra.cluster import Cluster
import redis

# Create your views here.

def index(request):
    cluster = Cluster('Test Cluster')
    session = cluster.connect('ecommerce')
    session.set_keyspace('produto')
    rows = session.execute('SELECT codigo, descricao, preco FROM produto')
    context = {'rows' : rows}
    return render(request, 'base.html', context)

def carrinho(request):
    context = {}
    return render(request, 'polls/index.html', context)

def fecharpedido(request):
    context = {}
    return render(request, 'polls/index.html', context)
