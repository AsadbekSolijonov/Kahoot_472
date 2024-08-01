from django.shortcuts import render


def home_view(request):
    return render(request, 'kahoot/home.html')


def detail_view(request):
    return render(request, 'kahoot/detail.html')
