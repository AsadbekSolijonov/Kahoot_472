from django.db import models
import random
import string


# 1. O'yin modeli
class Game(models.Model):
    pin_code = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=False)  # O'yin boshlangani yoki yo'qligi
    started = models.BooleanField(default=False)  # O'yin hozir boshlangani haqida

    def __str__(self):
        return self.pin_code

    def save(self, *args, **kwargs):
        if not self.pin_code:
            self.pin_code = ''.join(random.choices(string.digits, k=6))  # 6 xonali PIN yaratish
        super().save(*args, **kwargs)


# 2. O'yinchi modeli
class Player(models.Model):
    nickname = models.CharField(max_length=50)  # O'yinchi nomi
    game = models.ForeignKey(Game, related_name='players', on_delete=models.CASCADE)  # O'yinga bog'liq
    score = models.IntegerField(default=0)  # O'yinchining hozirgi balli
    joined_at = models.DateTimeField(auto_now=True)  # O'yinga kirgan vaqt

    def __str__(self):
        return f"{self.nickname} (Score: {self.score})"


class Category(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='cat_logo/')
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='questions')  # Kategoriya bilan bog'langan
    logo = models.ImageField(upload_to='quiz_logo/', blank=True, null=True)  # Savol logosi (ixtiyoriy)
    question = models.CharField(max_length=300)  # Savol matni
    time = models.PositiveSmallIntegerField(default=10)  # Savolga javob berish vaqti (soniyalar)

    def __str__(self):
        return self.question


# 5. Variantlar modeli (javob variantlari)
class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')  # Savol bilan bog'langan
    answer = models.CharField(max_length=300)  # Javob varianti matni
    is_correct = models.BooleanField(default=False)  # To'g'ri javob yoki yo'q

    def __str__(self):
        return self.answer


# 6. O'yinchining javoblari modeli
class PlayerAnswer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="answers")  # O'yinchi bilan bog'langan
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # Savol bilan bog'langan
    option = models.ForeignKey(Option, on_delete=models.CASCADE)  # O'yinchining tanlagan varianti
    answered_at = models.DateTimeField(auto_now_add=True)  # Javob berilgan vaqt

    def __str__(self):
        return f"{self.player.nickname} answered {self.option.answer} for {self.question.question}"
