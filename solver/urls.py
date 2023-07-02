from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('benchmark/', views.benchmark, name="benchmark"),
    path('manual/', views.manual, name="manual"),
    path('result/', views.result, name="result"),
]