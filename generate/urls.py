from django.urls import path
from . import views

app_name = 'generate'

urlpatterns = [
    path('', views.generate_view, name='generate'),
    path('generate-draft/', views.generate_draft, name='generate_draft'),
    path('get-progress/', views.get_progress, name='get_progress'),
    path('download/<str:filename>/', views.download_contract, name='download_contract'),
]