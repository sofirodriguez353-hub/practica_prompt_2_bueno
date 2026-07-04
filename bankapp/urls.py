from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('signup/', views.signup, name='signup'),
    path('movimiento/nuevo/', views.movimiento_create, name='movimiento_create'),
    path('movimiento/<int:pk>/editar/', views.movimiento_update, name='movimiento_update'),
    path('movimiento/<int:pk>/eliminar/', views.movimiento_delete, name='movimiento_delete'),
]
