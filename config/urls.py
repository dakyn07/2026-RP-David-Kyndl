from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('league/<str:league_code>/', views.league_view, name='league_view'),
    path('team/<int:team_id>/', views.team_detail, name='team_detail'),
]