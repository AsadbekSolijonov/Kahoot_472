from django.contrib import admin
from kahoot.models import Category, Question, Option

admin.site.register([Category, Option])


class OptionAdmin(admin.TabularInline):
    model = Option
    extra = 1
    max_num = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionAdmin]
