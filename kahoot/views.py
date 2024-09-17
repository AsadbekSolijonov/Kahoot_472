from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from kahoot.forms import CategoryForm, QuestionForm, OptionForm, OptionFormSet
from kahoot.models import Question, Category, Game


def home_view(request):
    categories = Category.objects.all()
    search = request.GET.get('search')
    if search:
        categories = categories.filter(title__icontains=search)
    context = {
        'categories': categories,
        'search': search if search else '',
    }
    return render(request, 'kahoot/home.html', context)


def detail_view(request, pk):
    category = get_object_or_404(Category, id=pk)
    context = {
        'category': category,
    }
    return render(request, 'kahoot/detail.html', context)


def list_create(request):
    category_form = CategoryForm()
    question_form = QuestionForm()
    option_form = OptionForm()
    option_formset = OptionFormSet()

    context = {
        'category_form': category_form,
        'question_form': question_form,
        'option_form': option_form,
        'option_formset': option_formset
    }
    return render(request, 'kahoot/list_create.html', context)


def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home-view')
        else:
            print(form.errors)
    category_form = CategoryForm()
    question_form = QuestionForm()
    option_form = OptionForm()
    option_formset = OptionFormSet()

    context = {
        'category_form': category_form,
        'question_form': question_form,
        'option_form': option_form,
        'option_formset': option_formset
    }
    return render(request, 'kahoot/list_create.html', context)


def create_question(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, request.FILES)
        option_formset = OptionFormSet(request.POST, instance=question_form.instance)

        if question_form.is_valid() and option_formset.is_valid():
            question_form.save()
            option_formset.save()
            return redirect('home-view')  # Replace with your success URL
        else:
            print(f":) option forms: {option_formset.errors}")
            print(f":) question forms: {question_form.errors}")

    question_form = QuestionForm()
    option_formset = OptionFormSet()

    return render(request, 'kahoot/list_create.html', {
        'question_form': question_form,
        'option_formset': option_formset,
    })


def game_themes(request):
    return render(request, 'kahoot/game_theme.html')


def game_pin(request):
    import random
    random_number = random.randint(100000, 1000000)
    context = {
        'random_number': str(random_number)[:3] + " " + str(random_number)[3:]
    }
    return render(request, 'kahoot/game_pin.html', context)


def quiz_page(request, game_id):
    # O'yin obyektini olish
    game = get_object_or_404(Game, pk=game_id)
    return render(request, 'kahoot/quizs.html', {'game': game})


def start_quiz(request, game_id):
    # O'yin obyektini olish
    game = get_object_or_404(Game, pk=game_id)

    # O'yin boshlanmagan bo'lsa, uni boshlash
    if not game.started:
        game.started = True
        game.save()

    # Quizlarni olish (bu yerda `Category` modeliga asoslangan)
    questions = Question.objects.filter(category__in=Category.objects.filter(questions__game=game)).order_by('id')

    # Foydalanuvchini quiz sahifasiga yo'naltirish
    return render(request, 'kahoot/quizs.html', {'game': game, 'questions': questions})


def join_game(request):
    return render(request, 'kahoot/join_game.html')


# View for creating a game
def create_game(request):
    if request.method == 'POST':
        game = Game.objects.create(is_active=True)
        return redirect('waiting_room', pin_code=game.pin_code)
    return render(request, 'create_game.html')


# Waiting room view (no changes in the backend for WebSockets)
def waiting_room(request, pin_code):
    game = get_object_or_404(Game, pin_code=pin_code, is_active=True)
    players = game.players.all()
    return render(request, 'waiting_room.html', {'game': game, 'players': players})


# View to start the game (via WebSocket for real-time)
def start_game(request, pin_code):
    game = get_object_or_404(Game, pin_code=pin_code, is_active=True)
    if game:
        return redirect('game_started')  # Redirect to the game started page
    return JsonResponse({"error": "Game could not be started"}, status=400)
