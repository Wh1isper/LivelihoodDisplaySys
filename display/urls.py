from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('query/count', views.query_count, name = 'count'),
    path('init', views.init, name='init')
]
