from django.urls import path
from . import views

urlpatterns = [

    path('movies/',views.MoviesListCreateView.as_view()),
    
    path('movies/<str:uuid>/',views.MoviesRetrieveUpdateDestroyView.as_view()),

    path('rating/<str:uuid>/',views.AddRatingView.as_view()),
    
]