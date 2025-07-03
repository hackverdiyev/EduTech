from django.conf.urls.static import static
from django.urls import path,include
from django.contrib import admin
from django.conf import settings
from base import views
from problems import views as problems_views
from groups import views as groups_views
from django.views.static import serve
from django.urls import include, re_path

urlpatterns = [
    path('admin/',views.admin_page),
    path('admin/bc91b7c47993de857e161b3984d195672153b07b2243b7a5838cc189cb677aa3/', admin.site.urls),
    path('', include('base.urls')),
    path('ranking/', problems_views.ranking, name='ranking'),
    path('problems/', include('problems.urls')),
    path('groups/', include('groups.urls')),
    path('add/', problems_views.add_problem, name="add_problem"),
    path('add/<int:problem_id>/', problems_views.add_solution, name="add_solution"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

