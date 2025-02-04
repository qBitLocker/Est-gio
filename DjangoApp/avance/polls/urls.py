from django.urls import path 

from . import views 

app_name = "polls"

urlpatterns = [
    # Fora do tutorial
    path("consulta/", views.consulta, name="consulta"),
    path("cadastro/", views.cadastro, name="cadastro"),
    path("login/", views.login, name="login"),
    path("home/", views.home, name="home")
]