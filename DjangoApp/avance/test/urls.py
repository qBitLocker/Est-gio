from django.urls import path

from . import views 

urlpatterns = [
    # A rota /index será registrada utilizando como referencia path("test", include('test.urls'))
    # Ou seja, para acessa o views.index é necessário test/index
    #path("/index", views.index, name="test_index")

    # Acessar em test
    path("", views.index)
]