# index/urls.py
from django.urls import path
from . import views

app_name = 'index'  # 添加命名空间

urlpatterns = [
    path('', views.index_view, name='index'),
]