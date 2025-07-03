from django.urls import path
from . import views

urlpatterns = [
    path('', views.problems_main, name="problems_main"),
    path('<str:subject>/', views.problems, name='problems'),
    path('<str:subject>/<int:id>/', views.problem_view, name='problem_view'),
]