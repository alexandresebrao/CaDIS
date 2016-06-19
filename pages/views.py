# coding: utf-8
# DJANGO
from django.shortcuts import render
import simplejson as json
from django.http import HttpResponse, JsonResponse

# DataBase
from cassandra.cluster import Cluster
import redis


# Create your views here.
def index(request):
    # CONNECT TO PYTHON - CASSANDRA#
    cluster = Cluster()
    session = cluster.connect('ecommerce')
    rows = session.execute('SELECT codigo, descricao, preco FROM produto')
    context = {'rows': rows}
    print request.session.session_key
    return render(request, 'base.html', context)


def carrinho(request):
    context = {}
    return render(request, 'polls/index.html', context)


def fecharpedido(request):
    context = {}
    return render(request, 'polls/index.html', context)


def ajax(request):

    cluster = Cluster()
    session = cluster.connect('ecommerce')
    rows = session.execute('SELECT codigo, descricao, preco FROM produto')
    lista = []
    for row in rows:
        dicto = {}
        dicto['name'] = row.descricao
        dicto['price'] = row.preco
        lista.append(dicto)
    return JsonResponse(lista, safe=False)
