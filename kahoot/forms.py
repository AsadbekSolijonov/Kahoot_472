from django import forms
from django.forms.models import inlineformset_factory
from kahoot.models import Category, Question, Option


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['author', 'logo', 'title', 'description']
        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['category', 'question', 'logo', 'time']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'time': forms.TextInput(attrs={'class': 'form-control'}),
        }


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['question', 'answer', 'is_correct']
        widgets = {
            'question': forms.Select(attrs={'class': 'form-control'}),
            'answer': forms.TextInput(attrs={'class': 'form-control'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


OptionFormSet = inlineformset_factory(
    Question, Option, form=OptionForm, extra=4, max_num=4, can_delete=True
)
