from django.urls import path

from . import views


urlpatterns = [

    path('movies/',views.MoviesListCreateView.as_view()),

]