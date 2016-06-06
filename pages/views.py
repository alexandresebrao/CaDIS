<<<<<<< HEAD
from django.shortcuts import render

# Create your views here.
=======
#DJANGO
from django.shortcuts import render

#DataBase
from cassandra.cluster import Cluster
import redis

# Create your views here.

def index(request):
    context = {}
    return render(request, 'base.html', context)

def carrinho(request):
    context = {}
    return render(request, 'polls/index.html', context)

def fecharpedido(request):
    context = {}
    return render(request, 'polls/index.html', context)
