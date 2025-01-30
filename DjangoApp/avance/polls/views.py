from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Product

# Create your views here.
def index(request):
    return HttpResponse ("<h1>Hello, World</h1>")

# Novos views -> Adicionar em polls/urls.py
def detail(request, id):
    return HttpResponse("You're looking at question %s." % id)

# Pesquisar como /polls{id}
def results(request, id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % id)

def vote(request, id):
    return HttpResponse("You're voting on question %s." % id)

def fetch (request):
    # Adquire todos os objetos e retorna para o usuário
    # result = Product.objects.all()
    # return HttpResponse(result)
    products = Product.objects.all()
    template = loader.get_template('polls/index.html')
    context = {
        'products': products
    }

    return HttpResponse(template.render(context, request))

def service(request):
    
    if request.method == "POST":
        # return HttpResponse('<h1>Processing POST request</h1>')
        context = {
            'is_post': True
        }
        return render(request, 'polls/detail.html', context)
    elif request.method == "GET":
        #return HttpResponse('<h1>Processing GET request</h1>')
        return render(request, 'polls/detail.html')
    else:
        return HttpResponse('<h1>Invalid Request</h1>')