from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.db.models import F
from django.urls import reverse

from .models import Product, Question, Choice, User
from security.cipher_algo import CipherTools


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
def detail(request, question_id):
    '''try:
        question = Question.objects.get(pk=id)
    except (Question.DoesNotExist):
        raise Http404("Question {} does not exist".format(id))
    return render(request, "polls/detail.html", {
        "question": question
    })'''
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/tutorial4.html", {
        "question":question
    })


# Pesquisar como /polls{id}
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    # Verificar se polls/x/vote, x é uma chave cadastrada na tabela
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
########################## Interface fora do tutorial #######################################

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
    
####################################### tela de login ##############################################
def signup (request):
    if request.method == "POST":
        # Captura dos campos do formulário
        username = request.POST['username']
        password = request.POST['password']

        # Criação de um objeto CipherTools
        cipher = CipherTools()
        hashed = cipher.Bcrypt_enc(password.encode())

        # Criação do modelo de usuário 
        user = User(username=username, password=hashed)

        # Inserção do usuário no banco de dados
        user.save()

        # Redirecionamento para a página de login
        return render(request, "polls/login.html", {
            "success": True,
            "message": "Usuário cadastrado com sucesso"
        })

    elif request.method == "GET":
        return render(request, "polls/cadastro.html")



def login(request):
    if request.method == "GET":
        return render(request, "polls/login.html")
    
def home(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.filter(username=username)
            cipher = CipherTools()
            if cipher.Bcrypt_match(password.encode(), user[0].password):
                return render(request, "polls/home.html", {
                    "login_status": "Sucess"
                })
            else:
                return render(request, "polls/login.html", {
                    "error": True,
                    "message": "Senha errada"
                })
        except (Exception, User.DoesNotExist):
            return render(request, "polls/login.html", {
                "error": True,
                "message": "Usuário não encontrado no banco de dados"
            })
    elif request.method == "GET":
        return HttpResponse("<h1>Bem vindo a home page</h1>")
