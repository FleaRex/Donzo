from django.urls import path

from . import views

app_name = 'jeerer_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('card/<int:card_id>/', views.card, name='card'),
    path('card/', views.card_create, name='card_create'),
]