from django.db import models
import random
import string


# 1. O'yin modeli
class Game(models.Model):
    pin_code = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=False)
    started = models.BooleanField(default=False)

    def __str__(self):
        return self.pin_code

    def save(self, *args, **kwargs):
        if not self.pin_code:
            self.pin_code = ''.join(random.choices(string.digits, k=6))  # Generates a 6-digit game PIN
        super().save(*args, **kwargs)


# 2. O'yinchi modeli
class Player(models.Model):
    nickname = models.CharField(max_length=50)
    game = models.ForeignKey(Game, related_name='players', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    joined_at = models.DateTimeField(auto_now=True)  # O'yinga qo'shilgan vaqt

    def __str__(self):
        return f"{self.nickname} (Score: {self.score})"


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
