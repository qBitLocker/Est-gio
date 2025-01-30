from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Product, Question, Choice

# Create your views here.
def index(request):
    # Ultimas 5 publicacoes
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    output = ", ".join([q.question_text for q in latest_question_list])
    return HttpResponse(output)

    # Renderizar em template?
    ''' context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)'''

# Novos views -> Adicionar em polls/urls.py
def detail(request, id):
    '''try:
        question = Question.objects.get(pk=id)
    except (Question.DoesNotExist):
        raise Http404("Question {} does not exist".format(id))
    return render(request, "polls/detail.html", {
        "question": question
    })'''
    question = get_object_or_404(Question, pk=id)
    return render(request, "polls/detail.html", {
        "question":question
    })


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
        codbar = request.POST['codbar']
        context = { 'is_post': True }
        try:
            # pk = primary key
            product = Product.objects.get(id=codbar)
            context['product'] = product
        except (KeyError, Product.DoesNotExist):
            context['product'] = None
        
        return render(request, 'polls/detail.html', context)
    elif request.method == "GET":
        #return HttpResponse('<h1>Processing GET request</h1>')
        return render(request, 'polls/detail.html')
    else:
        return HttpResponse('<h1>Invalid Request</h1>')