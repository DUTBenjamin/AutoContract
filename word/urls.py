from django.urls import path
from. import views

urlpatterns = [
    path('', views.word_view, name='word'),
]