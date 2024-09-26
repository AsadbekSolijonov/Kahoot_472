import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from kahoot.forms import CategoryForm, QuestionForm, OptionForm, OptionFormSet
from kahoot.models import Question, Category, Game, Option, Player, PlayerAnswer


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


# View for creating a game
# Create a new game
def create_game(request):
    if request.method == 'POST':
        game = Game.objects.create(is_active=True)
        return redirect('game_waiting_room', pin_code=game.pin_code)
    return render(request, 'create_game.html')


def waiting_room(request, pin_code):
    game = get_object_or_404(Game, pin_code=pin_code, is_active=True)

    if request.method == 'POST' and request.POST.get('action') == 'join':
        nickname = request.POST.get('nickname')
        if nickname:
            if not Player.objects.filter(nickname=nickname, game=game).exists():
                player = Player.objects.create(nickname=nickname, game=game)
                request.session['player_id'] = player.id  # Store player ID in session
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "error", "message": "Nickname already exists"})
        else:
            return JsonResponse({"status": "error", "message": "Nickname cannot be empty"})

    elif request.method == 'POST' and request.POST.get('action') == 'remove':
        player_id = request.POST.get('player_id')
        player = Player.objects.filter(id=player_id, game=game).first()

        data = json.loads(request.body)
        categoryId = data.get('categoryId')
        print(categoryId)

        category = Category.objects.get(id=3)
        category.game = game
        category.save()
        if player:
            player.delete()
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error", "message": "Player not found"})

    players = game.players.all()
    return render(request, 'waiting_room.html', {'game': game, 'players': players})


def start_game(request, pin_code):
    game = get_object_or_404(Game, pin_code=pin_code, is_active=True)

    if game:
        game.started = True
        game.save()

        # Redirect to a new view where questions are displayed
        return redirect('game_started', pin_code=game.pin_code)

    return JsonResponse({"error": "Game could not be started"}, status=400)


def game_started(request, pin_code):
    game = get_object_or_404(Game, pin_code=pin_code, started=True)
    player_id = request.session.get('player_id')

    if not player_id:
        return redirect('game_waiting_room', pin_code=pin_code)

    player = get_object_or_404(Player, id=player_id, game=game)

    # Fetch the first question for the game
    questions = Question.objects.filter(category__game=game)

    if not questions.exists():
        return JsonResponse({"error": "No questions available for this game."}, status=400)

    first_question = questions.first()

    return render(request, 'game_started.html', {
        'game': game,
        'question': first_question,
        'options': first_question.options.all(),
        'player': player,
    })


def submit_answer(request, question_id, player_id):
    question = get_object_or_404(Question, id=question_id)
    player = get_object_or_404(Player, id=player_id)

    if request.method == 'POST':
        selected_option_id = request.POST.get('option_id')
        selected_option = Option.objects.filter(id=selected_option_id, question=question).first()

        if selected_option and selected_option.is_correct:
            player.score += 10
            player.save()
            return JsonResponse({"status": "correct", "score": player.score})
        else:
            return JsonResponse({"status": "incorrect"})

    return JsonResponse({"status": "error"})


def game_scoreboard(request, pin_code):
    game = get_object_or_404(Game, pin_code=pin_code, started=True)
    players = game.players.order_by('-score')
    return render(request, 'scoreboard.html', {'game': game, 'players': players})
