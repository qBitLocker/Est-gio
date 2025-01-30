from django.urls import path 

from . import views 

app_name = "polls"

urlpatterns = [
    # Implementando o conceito de Generic Views
    #path("", views.IndexView.as_view(), name="index"),

    path("", views.index, name="index"),
    path("/", views.index, name="index"),

    # ex: /polls/5
    path("/<int:id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("/<int:id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("/<int:id>/vote/", views.vote, name="vote"),

    
    
    
    # Fora do tutorial
    path("/fetch", views.fetch, name="fetch"),

    path("/service", views.service, name='service')
]