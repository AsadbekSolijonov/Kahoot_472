from django.urls import path
from kahoot import views

urlpatterns = [
    path('', views.home_view, name='home-view'),
    path('detail/<int:pk>', views.detail_view, name='detail-view'),
    path('list-create/', views.list_create, name='list-create'),
    path('category-create/', views.category_create, name='category-create'),
    path('question-create/', views.create_question, name='question-create'),
    path('game-themes/', views.game_themes, name='game-themes'),
    path('game-pin/', views.game_pin, name='game-pin'),

]
