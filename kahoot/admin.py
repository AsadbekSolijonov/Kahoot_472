from django.contrib import admin
from kahoot.models import Category, Question, Option, Game, Player

admin.site.register([Category, Option])


class OptionAdmin(admin.TabularInline):
    model = Option
    extra = 1
    max_num = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionAdmin]


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['id', 'pin_code', 'is_active', 'started']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'game', 'score', 'joined_at']
