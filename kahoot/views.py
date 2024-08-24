from django.shortcuts import render, get_object_or_404, redirect

from kahoot.forms import CategoryForm, QuestionForm, OptionForm, OptionFormSet
from kahoot.models import Question, Category


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
