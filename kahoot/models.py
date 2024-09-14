from django.db import models


# 1. O'yin modeli
class Game(models.Model):
    pin = models.CharField(max_length=6, unique=True)  # Game PIN
    title = models.CharField(max_length=255, default="Kahoot O'yini")  # O'yin nomi
    started_at = models.DateTimeField(null=True, blank=True)  # O'yin boshlanish vaqti
    ended_at = models.DateTimeField(null=True, blank=True)  # O'yin tugash vaqti
    is_active = models.BooleanField(default=True)  # O'yin faollik holati

    def __str__(self):
        return f"{self.title} - PIN: {self.pin}"


# 2. O'yinchi modeli
class Player(models.Model):
    username = models.CharField(max_length=50)  # O'yinchining ismi
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="players")  # O'yin bilan bog'lanish
    score = models.IntegerField(default=0)  # O'yinchi ballari
    joined_at = models.DateTimeField(auto_now=True)  # O'yinga qo'shilgan vaqt

    def __str__(self):
        return f"{self.username} (Score: {self.score})"


class Category(models.Model):
    author = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='cat_logo/')
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
    logo = models.ImageField(upload_to='quiz_logo/')
    question = models.CharField(max_length=300)
    time = models.PositiveSmallIntegerField(default=10)

    def __str__(self):
        return self.question


class Option(models.Model):
    # player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="answers")  # O'yinchi bilan bog'lanish
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    answer = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer
