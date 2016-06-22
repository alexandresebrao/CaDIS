# coding: utf-8
# DJANGO
from django.shortcuts import render, redirect
import simplejson as json
from django.http import HttpResponse, JsonResponse
import random
# DataBase
from cassandra.cluster import Cluster
from cassandra.query import named_tuple_factory, dict_factory

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
        produto['preco'] = r.hgetall(i)['preco']
        produto['codigo'] = r.hgetall(i)['codigo']
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
    i = r.hgetall('produto:%s' % produto.replace(' ','_'))
    produto_car = {}
    produto_car['nome'] = produto
    produto_car['preco'] = i['preco']
    produto_car['codigo'] = i['codigo']
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
    somatorio = 0.0
    for i in lista:
        carrinho.append(r.hgetall(i))
        somatorio += float(r.hgetall(i)['preco'])
    context['carrinho'] = carrinho
    context['totalcompra'] = somatorio
    return render(request, 'carrinho.html', context)


def limpar_carrinho(request):
    r = redis.Redis(host='redis.kdalegends.me', port=6379, password='aulaivo')
    try:
        request.session['user']
    except:
        request.session['user'] = random.getrandbits(128)
    string = 'carrinho:%s:*' % request.session['user']
    lista = r.keys(string)
    for i in lista:
        r.delete(i)
    return redirect('/')

def finalizar(request):
    cluster = Cluster()
    session = cluster.connect('ecommerce')
    r = redis.Redis(host='redis.kdalegends.me', port=6379, password='aulaivo')
    try:
        request.session['user']
    except:
        request.session['user'] = random.getrandbits(128)
    string = 'carrinho:%s:*' % request.session['user']
    session.row_factory = dict_factory
    row = session.execute('SELECT max(codigo_tran) FROM pedido LIMIT 1')
    codigo_tran = int(row[0]['system.max(codigo_tran)'])
    row = session.execute('SELECT max(cod_pedido) FROM pedido LIMIT 1')
    codigo_pedido = int(row[0]['system.max(cod_pedido)']) + 1
    cpf = request.POST['cpf']
    lista = r.keys(string)
    for i in lista:
        codigo_tran += 1
        item = r.hgetall(i)
        string_cql = "insert into pedido (codigo_tran, cod_pedido , cpf , data , produto , quantidade) values (%s, %s, %s, %s,%s, 1);" % (codigo_tran, codigo_pedido, cpf, datetime.now(), item['codigo'])
    return redirect('/limpar_carrinho/')


def admin(request):
    r = redis.Redis(host='redis.kdalegends.me', port=6379, password='aulaivo')
    try:
        request.session['user']
    except:
        request.session['user'] = random.getrandbits(128)
    return None
