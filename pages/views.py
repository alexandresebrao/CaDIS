# coding: utf-8
# DJANGO
from django.shortcuts import render, redirect
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
    return render(request, 'base.html', context)


def carrinho(request, produto):
    try:
        request.session['user']
    except:
        request.session['user'] = random.getrandbits(128)
    # Primeiramente vamos ver os produtos do usuario no carrinho
    r = redis.Redis(host='redis.kdalegends.me', port=6379, password='aulaivo')
    print produto
    string = 'carrinho:%s:*' % request.session['user']
    lista = r.keys(string)
    string = 'carrinho:%s:%s' % (request.session['user'], len(lista))
    string_valor = 'produto:%s' % (produto.replace(' ', '_'))
    produto_car = {}
    produto_car['nome'] = string_valor
    produto_car['preco'] = r.get(string_valor)
    r.hmset(string, produto_car)

    return redirect('/carrinho/')


def mostrar_carrinho(request):
    try:
        request.session['user']
    except:
        request.session['user'] = random.getrandbits(128)
    context = {}
    r = redis.Redis(host='redis.kdalegends.me', port=6379, password='aulaivo')
    carrinho = []
    string = 'carrinho:%s:*' % request.session['user']
    lista = r.keys(string)
    for i in lista:
        carrinho.append(r.hgetall(i))
    context['carrinho'] = carrinho
    return render(request, 'carrinho.html', context)
