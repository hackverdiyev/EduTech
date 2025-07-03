from django.urls import path
from . import views

urlpatterns = [
    path('', views.groups_main, name="groups_main"),
    path('<int:id>/', views.groups, name="groups"),
    path('create/', views.create_group, name="create_group"),
    path('<int:id>/contests/<int:contest_id>/', views.contests, name="contests"),
]
