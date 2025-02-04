from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.db.models import F
from django.urls import reverse

# Importação dos models
from .models import Product, User
from security.cipher_algo import CipherTools

def consulta(request):
    if request.method == "POST":
        product_id = request.POST['product_id']
        print(product_id)
        try:
            # pk = primary key
            product = Product.objects.get(id=product_id)

            context = {'product': product}

        except (KeyError, Product.DoesNotExist):
            context = {'product': None}
        
        return render(request, 'polls/consulta.html', context)
    elif request.method == "GET":
        #return HttpResponse('<h1>Processing GET request</h1>')
        return render(request, 'polls/consulta.html')
    else:
        return HttpResponse('<h1>Invalid Request</h1>')

def cadastro (request):
    if request.method == "POST":
        # Captura dos campos do formulário
        username = request.POST['username']
        password = request.POST['password']

        if not User.objects.filter(username=username).exists():
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
        else:
            return render(request, "polls/cadastro.html", {
                "error": True,
                "message": "Usuário já cadastrado"
            })

    elif request.method == "GET":
        return render(request, "polls/cadastro.html")

def login(request):
    if request.method == "GET":
        return render(request, "polls/login.html")

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Validando o usuário e a senha
        try:
            user = User.objects.get(username=username)
            cipher = CipherTools()
            if cipher.Bcrypt_match(password.encode(), user.password):
                return redirect('polls:consulta')
                #return render(request, "polls/consulta.html")
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
    else:
        return HttpResponse('<h1>Invalid Request</h1>')



def home(request):
    if request.method == "POST":


        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.filter(username=username)
            cipher = CipherTools()
            if cipher.Bcrypt_match(password.encode(), user[0].password):
                return render(request, "polls/consulta.html")
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
