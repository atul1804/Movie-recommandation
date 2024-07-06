from django.urls import path
from . import views

urlpatterns = [
    path('genresearch/', views.genresearch, name='genresearch'),
    path('showmovies/', views.showmovies, name='showmovies'),
    path('moviesearch/', views.moviesearch, name='moviesearch'),
    path('titleshow/', views.titleshow, name='titleshow'),
]