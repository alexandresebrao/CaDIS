# coding: utf-8
# DJANGO
from django.shortcuts import render
import simplejson as json
from django.http import HttpResponse, JsonResponse
import random
# DataBase
from cassandra.cluster import Cluster
import redis


# Create your views here.
def index(request):
    # CONNECT TO PYTHON - CASSANDRA#
    # cluster = Cluster()
    # session = cluster.connect('ecommerce')
    # rows = session.execute('SELECT codigo, descricao, preco FROM produto')
    # context = {'rows': rows}
    r = redis.Redis(host='redis.kdalegends.me', port=6379, password='aulaivo')
    lista = r.keys('produto:*')
    produtos = []
    context = {}
    for i in lista:
        produto = {}
        produto['nome'] = i.replace('produto:', '').replace('_', ' ')
        produto['preco'] = r.get(i)
        produtos.append(produto)
    try:
        request.session['user']
    except:
        request.session['user'] = random.getrandbits(128)
    context['produtos'] = produtos
    print produtos
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
