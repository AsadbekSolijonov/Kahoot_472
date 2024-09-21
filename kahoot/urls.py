from django.urls import path
from kahoot import views
from kahoot.views import create_game, waiting_room, start_game, game_started, submit_answer, game_scoreboard

urlpatterns = [
    path('', views.home_view, name='home-view'),  # barcha kategoriyani ko'rish.
    path('detail/<int:pk>', views.detail_view, name='detail-view'),  # kategoriyaga tegishli savollarni ko'rish uchun.
    path('list-create/', views.list_create, name='list-create'),  # Yaratish bo'limi
    path('category-create/', views.category_create, name='category-create'),  # Kategoriya yaratish uchun.
    path('question-create/', views.create_question, name='question-create'),  # Savol va javoblar qo'shish
    path('game-themes/', views.game_themes, name='game-themes'),  # o'yin menyularini tanlash
    path('game-pin/', views.game_pin, name='game-pin'),

    path('create/', create_game, name='create_game'),
    path('waiting_room/<str:pin_code>/', waiting_room, name='game_waiting_room'),
    path('start/<str:pin_code>/', start_game, name='start_game'),
    path('game/<str:pin_code>/', game_started, name='game_started'),
    path('submit_answer/<int:question_id>/<int:player_id>/', submit_answer, name='submit_answer'),
    path('scoreboard/<str:pin_code>/', game_scoreboard, name='game_scoreboard'),
]
