from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>Hello, World from test</h1>")