from django.urls import path
from kahoot import views

urlpatterns = [
    path('', views.home_view, name='home-view'),  # barcha kategoriyani ko'rish.
    path('detail/<int:pk>', views.detail_view, name='detail-view'),  # kategoriyaga tegishli savollarni ko'rish uchun.
    path('list-create/', views.list_create, name='list-create'),  # Yaratish bo'limi
    path('category-create/', views.category_create, name='category-create'),  # Kategoriya yaratish uchun.
    path('question-create/', views.create_question, name='question-create'),  # Savol va javoblar qo'shish
    path('game-themes/', views.game_themes, name='game-themes'),  # o'yin menyularini tanlash
    path('quizs/', views.quiz_page, name='quizs'),  # savollarni detail ko'rsatish
    path('game-pin/', views.game_pin, name='game-pin'),

    path('create-game/', views.create_game, name='create_game'),
    path('waiting-room/<str:pin_code>/', views.waiting_room, name='waiting_room'),
    path('start-game/<str:pin_code>/', views.start_game, name='start_game'),

]
