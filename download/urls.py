# download/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('download/', views.download_view, name='download'),
    path('get-contracts/', views.get_contracts, name='get_contracts'),
    path('download/<str:filename>/', views.download_contract, name='download_contract'),
]