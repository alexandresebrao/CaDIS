# -*- coding: utf-8 -*-

import redis
from cassandra.cluster import Cluster
from cassandra.query import named_tuple_factory
cluster = Cluster()
session = cluster.connect('ecommerce')
session.row_factory = named_tuple_factory
produtos = session.execute('SELECT codigo, descricao, preco, quantidade FROM produto')
r = redis.Redis(host='redis.kdalegends.me', port = 6379, password='aulaivo')

# Criar key produto:"nome_do_produto" com valor "código_do_produto"
for produto in produtos:
	print "-----"
	print produto.descricao
	print produto.preco
	print produto.codigo
	print "-----"
	string = "produto:%s" % (produto.descricao.replace(' ', '_'))
	print string
	valor = {}
	valor['codigo'] = produto.codigo
	valor['preco'] = produto.preco
	r.hmset(string, valor)
