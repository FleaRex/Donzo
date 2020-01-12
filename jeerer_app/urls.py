from django.urls import path

from . import views

app_name = 'jeerer_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('board/', views.board_create, name='board_create'),
    path('board/<int:board_id>/', views.board, name='board'),
    path('board/<int:board_id>/card/', views.card_create, name='card_create'),
    path('board/<int:board_id>/card/<int:card_id>/', views.card, name='card'),
    path('board/<int:board_id>/card/<int:card_id>/delete/', views.card_delete, name='card_delete'),
    path('board/<int:board_id>/card/<int:card_id>/children/', views.children, name='children'),
    path('board/<int:board_id>/card/<int:card_id>/done/', views.mark_done, name='mark_done'),
]