from django.shortcuts import render, get_object_or_404

from kahoot.forms import CategoryForm, QuestionForm, OptionForm
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

    context = {
        'category_form': category_form,
        'question_form': question_form,
        'option_form': option_form,
    }
    return render(request, 'kahoot/list_create.html', context)
