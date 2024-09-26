from django.contrib import admin
from nested_admin.nested import NestedTabularInline, NestedStackedInline, NestedModelAdmin

from kahoot.models import Category, Question, Option, Game, Player


class OptionAdmin(NestedTabularInline):
    model = Option
    fields = ('answer', 'is_correct')
    extra = 0
    max_num = 4


class QuestionAdmin(NestedStackedInline):
    model = Question
    extra = 0
    fields = ('logo', 'question', 'time')
    inlines = [OptionAdmin]


@admin.register(Category)
class CategoryAdmin(NestedModelAdmin):
    inlines = [QuestionAdmin]
    list_display = ['id', 'title']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['id', 'pin_code', 'is_active', 'started']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'nickname', 'game', 'score', 'joined_at']
